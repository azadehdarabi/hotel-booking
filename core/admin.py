from django.contrib import admin

from core.models import Hotel, Room, Reservation


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'capacity')
    list_filter = ('hotel', 'capacity')
    search_fields = ('hotel__name',)
    raw_id_fields = ('hotel',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'guest', 'start_at', 'end_at')
    list_filter = ('room__hotel', 'start_at', 'end_at')
    search_fields = ('room__hotel__name', 'guest__username')
    raw_id_fields = ('room', 'guest')
