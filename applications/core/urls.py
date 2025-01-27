from django.urls import path
from .views import HotelListView, CreateReservationView

urlpatterns = [
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('reservation/', CreateReservationView.as_view(), name='reservation'),
]
