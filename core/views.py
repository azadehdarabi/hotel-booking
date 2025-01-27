from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.paginator import ResponsePaginator
from .models import Hotel
from .serializers import ReservationSerializer, HotelSerializer
from .utils import ReservationHttpResponseHandler


class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    pagination_class = ResponsePaginator


class CreateReservationView(generics.GenericAPIView):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    reservation_http_response_handler = ReservationHttpResponseHandler()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        hotel_id = serializer.validated_data['hotel_id']
        start_at = serializer.validated_data['start_at']
        end_at = serializer.validated_data['end_at']
        guest = self.request.user

        hotel = get_object_or_404(Hotel, id=hotel_id)
        reserve_id, result = hotel.reserve_room(guest=guest, start_at=start_at, end_at=end_at)

        response = self.reservation_http_response_handler.get_response(result)

        if reserve_id:
            return Response({'detail': response.detail, 'reservation_id': reserve_id}, status=response.status_code)

        return Response({'detail': response.detail}, status=response.status_code)
