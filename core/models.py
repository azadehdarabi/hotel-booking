from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from core.choices import HotelReservationMethodResults


class Hotel(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    class Meta:
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotels")
        ordering = ["-created_time"]

    def __str__(self):
        return self.name

    def reserve_room(self, guest, start_at, end_at):
        available_room = None
        with transaction.atomic():
            rooms = self.rooms.all()
            for room in rooms:
                overlapping_reservations = Reservation.objects.filter(
                    room=room,
                    start_at__lt=end_at,
                    end_at__gt=start_at
                ).select_for_update()

                if not overlapping_reservations.exists():
                    available_room = room
                    break

            if not available_room:
                return None, HotelReservationMethodResults.FULL_ROOMS

            reservation = Reservation.objects.create(
                room=available_room,
                guest=guest,
                start_at=start_at,
                end_at=end_at
            )

        return reservation.room.id, HotelReservationMethodResults.SUCCESSFUL_RESERVATION


class Room(BaseModel):
    hotel = models.ForeignKey(verbose_name=_("Hotel"), to=Hotel, on_delete=models.CASCADE, related_name='rooms')
    capacity = models.IntegerField(verbose_name=_("Capacity"), default=1)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return f"{self.hotel.name} - Room {self.id}"


class Reservation(BaseModel):
    room = models.ForeignKey(verbose_name=_("Room"), to=Room, on_delete=models.CASCADE, related_name='reservations')
    guest = models.ForeignKey(verbose_name=_("Guest"), to=User, on_delete=models.CASCADE)
    start_at = models.DateTimeField(verbose_name=_("Start-at"))
    end_at = models.DateTimeField(verbose_name=_("End-at"))

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_at__gt=models.F('start_at')),
                name='end_at_after_start_at'
            ),
            models.UniqueConstraint(
                fields=['room', 'start_at', 'end_at'],
                name='unique_reservation_per_room'
            )
        ]

    def __str__(self):
        return f"{self.guest.username} - {self.room.id} - {self.start_at}"
