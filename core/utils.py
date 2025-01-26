from collections import namedtuple

from django.utils.translation import gettext_lazy as _
from rest_framework import status

response = namedtuple('Response', ['status_code', 'detail'])


class ReservationHttpResponseHandler:
    BAD_REQUEST = response(status.HTTP_400_BAD_REQUEST, _('Bad Request.'))
    FULL_ROOMS = response(status.HTTP_400_BAD_REQUEST, _("No rooms available for the given dates."))
    SUCCESSFUL_RESERVATION = response(status.HTTP_201_CREATED, _("Reservation successful."))

    def get_response(self, result):
        return getattr(self, result, 'BAD_REQUEST')
