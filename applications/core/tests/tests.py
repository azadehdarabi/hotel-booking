import concurrent.futures
import factory

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APITransactionTestCase

from applications.core.models import Reservation
from applications.core.tests.factories import UserFactory, HotelFactory, RoomFactory, ReservationFactory


class HotelReservationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory()

        cls.hotel_1, cls.hotel_2, cls.hotel_3 = HotelFactory.create_batch(3, name=factory.Iterator(
            ['Plaza', 'California', 'Hilton']))
        (cls.room_1, cls.room_2, cls.room_3,
         cls.room_4, cls.room_5, cls.room_6) = RoomFactory.create_batch(6, hotel=factory.Iterator(
            [cls.hotel_1, cls.hotel_2, cls.hotel_3]))
        ReservationFactory(room=cls.room_1, guest=cls.user_1, start_at=timezone.now() + timezone.timedelta(days=1),
                           end_at=timezone.now() + timezone.timedelta(days=4))

        cls.client = APIClient()

    def setUp(self):
        self.client.force_authenticate(user=self.user_1)

    def test_list_hotels(self):
        """Test the hotel listing API"""
        url = reverse('hotel-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 3)

        hotel_names = [hotel['name'] for hotel in response.data['results']]
        self.assertTrue('Plaza' in hotel_names)
        self.assertTrue('California' in hotel_names)
        self.assertTrue('Hilton' in hotel_names)

    def test_create_reservation_success(self):
        """Test creating a reservation successfully"""
        url = reverse('reservation')
        data = {
            "hotel_id": self.hotel_1.id,
            "start_at": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "end_at": (timezone.now() + timezone.timedelta(days=6)).isoformat()
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Reservation successful.')

        self.assertIn('reservation_id', response.data)

    def test_create_reservation_no_rooms_available(self):
        """Test creating a reservation when no rooms are available"""
        url = reverse('reservation')
        start_at = timezone.now() + timezone.timedelta(days=1)
        end_at = timezone.now() + timezone.timedelta(days=2)
        data = {
            "hotel_id": self.hotel_1.id,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat()
        }

        ReservationFactory(room=self.room_1, guest=self.user_1, start_at=start_at, end_at=end_at)
        ReservationFactory(room=self.room_4, guest=self.user_1, start_at=start_at, end_at=end_at)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'No rooms available for the given dates.')

    def test_create_reservation_invalid_start_date(self):
        """Test creating a reservation with invalid start date"""
        url = reverse('reservation')
        data = {
            "hotel_id": self.hotel_1.id,
            "start_at": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
            "end_at": (timezone.now() + timezone.timedelta(days=2)).isoformat()
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_at', response.data)

    def test_create_reservation_invalid_end_date(self):
        """Test creating a reservation with invalid end date"""
        url = reverse('reservation')
        data = {
            "hotel_id": self.hotel_1.id,
            "start_at": (timezone.now() + timezone.timedelta(days=4)).isoformat(),
            "end_at": (timezone.now() + timezone.timedelta(days=2)).isoformat()
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_at', response.data)

    def test_create_reservation_no_hotel(self):
        """Test creating a reservation with a non-existing hotel"""
        url = reverse('reservation')
        data = {
            "hotel_id": 999,
            "start_at": (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            "end_at": (timezone.now() + timezone.timedelta(days=6)).isoformat()
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No Hotel matches the given query.')


class ConcurrentReservationTestCase(APITransactionTestCase):
    def make_reservation(self, user, hotel_id, start_at, end_at):
        """Helper method to make reservation for a given user."""
        self.client.force_authenticate(user=user)
        url = reverse('reservation')
        data = {
            "hotel_id": hotel_id,
            "start_at": start_at.isoformat(),
            "end_at": end_at.isoformat()
        }
        return self.client.post(url, data, format='json')

    def test_concurrent_reservation(self):
        self.user_1, self.user_2 = UserFactory.create_batch(2)
        self.hotel_1 = HotelFactory(name="Plaza")
        self.room_1 = RoomFactory(hotel=self.hotel_1)
        self.client = APIClient()

        start_at = timezone.now() + timezone.timedelta(days=1)
        end_at = timezone.now() + timezone.timedelta(days=2)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_1 = executor.submit(self.make_reservation, self.user_1, self.hotel_1.id, start_at, end_at)
            future_2 = executor.submit(self.make_reservation, self.user_2, self.hotel_1.id, start_at, end_at)

            response_1 = future_1.result()
            response_2 = future_2.result()

        if response_1.status_code == status.HTTP_201_CREATED:
            successful_response = response_1
            failed_response = response_2
        else:
            successful_response = response_2
            failed_response = response_1

        self.assertEqual(successful_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(successful_response.data['detail'], 'Reservation successful.')

        self.assertEqual(failed_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(failed_response.data['detail'], 'No rooms available for the given dates.')

        self.assertEqual(Reservation.objects.filter(room=self.room_1).count(), 1)
