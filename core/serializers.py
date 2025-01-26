from django.utils import timezone
from rest_framework import serializers

from core.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name']


class ReservationSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()

    def validate(self, data):
        if data['start_at'] >= data['end_at']:
            raise serializers.ValidationError({"end_at": "finish must occur after start."})
        if data['start_at'] < timezone.now():
            raise serializers.ValidationError({"start_at": "Reservations cannot be made in the past."})
        return data
