from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class RoomStatus(IntegerChoices):
    EMPTY = 0, _("Empty")
    RESERVED = 1, _("RESERVED")


class HotelReservationMethodResults:
    FULL_ROOMS = 'FULL_ROOMS'
    SUCCESSFUL_RESERVATION = 'SUCCESSFUL_RESERVATION'
