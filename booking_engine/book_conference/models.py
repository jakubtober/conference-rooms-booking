from django.db import models
from datetime import date

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=64)
    seats = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def is_currently_booked(self):
        bookings_today = self.bookings.filter(date=date.today())
        return len(bookings_today) != 0

    def is_booked(self, date):
        bookings = self.bookings.filter(date=date)
        return len(bookings) != 0


class Booking(models.Model):
    room = models.ForeignKey(Room, related_name="bookings")
    date = models.DateField()
    comment = models.TextField(default='', blank=True)

    # class Meta:
    #     # nie będzie możliwości zarezerwowania tej samej sali na ten dzień
    #     unique_together = ("room", "date")

    def __str__(self):
        return str(self.date)


# room1 = Room.objects.create(name="Sala Chopin", seats=200, projector=True)
# room2 = Room.objects.create(name="Sala Bursztynowa", seats=100, projector=True)
# room3 = Room.objects.create(name="Sala Srebrna", seats=50, projector=True)
# room4 = Room.objects.create(name="Sala Zlota", seats=30, projector=True)

# Booking.objects.create(room_id=1)