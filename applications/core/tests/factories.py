import random
from datetime import timedelta

import factory
from django.contrib.auth.models import User
from django.utils import timezone
from factory.django import DjangoModelFactory

from applications.core.models import Hotel, Room, Reservation


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class HotelFactory(DjangoModelFactory):
    class Meta:
        model = Hotel

    name = factory.Sequence(lambda n: f"hotel_{n}")


class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    hotel = factory.SubFactory(HotelFactory)


class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation

    guest = factory.SubFactory(UserFactory)
    room = factory.SubFactory(RoomFactory)
    start_at = factory.lazy_attribute(lambda _: timezone.now() + timedelta(days=random.randint(1, 5)))
    end_at = factory.lazy_attribute(lambda _: timezone.now() + timedelta(days=random.randint(6, 10)))
