# Create your views here.
from django.views import View
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from book_conference.models import Room, Booking
from datetime import datetime


class RoomSearch(View):
    def get(self, request):
        date = datetime.today().strftime('%Y-%m-%d')

        return render(request, 'search.html', {
            'date': date,
        })

    def post(self, request):
        return HttpResponse('Sorry, POST no good...')


class SearchResults(View):
    def get(self, request):
        rooms = []
        user_date = request.GET.get('user_date')
        date = datetime.strptime(user_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        date_is_past = False
        user_seats = int(request.GET.get('seats'))
        room_name = request.GET.get('name')
        has_projector = request.GET.get('projector')
        projector = False

        if has_projector == 'yes':
            projector = True

        if date < datetime.today().strftime('%Y-%m-%d'):
            date = datetime.today().strftime('%Y-%m-%d')
            date_is_past = True

        rooms_matching_name = Room.objects.all().filter(Q(name__icontains=room_name), Q(seats__gte=user_seats), Q(projector=projector))

        for room in rooms_matching_name:
            if not room.is_booked(date) and not date_is_past:
                rooms.append(room)

        return render(request, 'search_results.html', {
            'date': date,
            'date_is_past': date_is_past,
            'rooms': rooms,
        })

    def post(self, request):
        pass


class Rooms(View):
    def get(self, request):

        rooms = Room.objects.all().order_by('name')
        date = datetime.today().strftime('%Y-%m-%d')

        booked_rooms = []
        not_booked_rooms = []

        for room in rooms:
            if room.is_booked(date):
                booked_rooms.append(room)
            else:
                not_booked_rooms.append(room)

        return render(request, 'rooms.html', {
            'date': date,
            'rooms': rooms,
            'booked_rooms': booked_rooms,
            'not_booked_rooms': not_booked_rooms,
        })

    def post(self, request):
        rooms = Room.objects.all().order_by('name')
        date_is_past = False

        user_date = request.POST.get('user_date')
        date = datetime.strptime(user_date, '%Y-%m-%d').strftime('%Y-%m-%d')

        if date < datetime.today().strftime('%Y-%m-%d'):
            date = datetime.today().strftime('%Y-%m-%d')
            date_is_past = True

        booked_rooms = []
        not_booked_rooms = []

        for room in rooms:
            if room.is_booked(date):
                booked_rooms.append(room)
            else:
                not_booked_rooms.append(room)

        return render(request, 'rooms.html', {
            'date_is_past': date_is_past,
            'date': date,
            'rooms': rooms,
            'booked_rooms': booked_rooms,
            'not_booked_rooms': not_booked_rooms,
        })


class RoomDetails(View):
    def get(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)
        bookings = room.bookings.filter(date__gte=datetime.today())

        return render(request, 'room_details.html', {
            'room': room,
            'bookings': bookings,
        })

    def post(self, room_id):
        pass


class NewRoom(View):
    def get(self, request):
        new_room = []
        return render(request, 'new_room.html', {
            'new_room': new_room,
        })

    def post(self, request):
        new_room = []
        has_projector = False
        name_of_the_new_room = request.POST.get('name')
        new_room_capacity = 0

        name_error = False
        seats_error = False

        if request.POST.get('seats'):
            new_room_capacity = int(request.POST.get('seats'))
        else:
            seats_error = True

        if new_room_capacity <= 0:
            seats_error = True

        if name_of_the_new_room.isspace() or name_of_the_new_room == '':
            name_error = True

        if request.POST.get('projector') == 'yes':
            has_projector = True

        if not name_error and not seats_error:
            new_room = Room.objects.create(name=name_of_the_new_room, seats=new_room_capacity, projector=has_projector)

        return render(request, 'new_room.html', {
            'new_room': new_room,
            'name_error': name_error,
            'seats_error': seats_error,
        })


class DeleteRoom(View):
    def get(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)


        return render(request, 'delete_room.html', {
            'room': room,
        })

    def post(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)
        delete_room = None
        return_to_homepage = False

        if request.POST.get('confirmation') == 'Yes':
            delete_room = True
        elif request.POST.get('confirmation') == 'No':
            return_to_homepage = True

        if delete_room == True:
            room.delete()

        return render(request, 'delete_room.html', {
            'room': room,
            'delete_room': delete_room,
            'return_to_homepage': return_to_homepage,
        })


class ModifyRoom(View):
    def get(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)
        is_room_updated = False

        return render(request, 'modify_room.html', {
            'room': room,
            'is_room_updated': is_room_updated,
        })

    def post(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)
        has_projector = False
        is_room_updated = False
        name_error = False
        seats_error = False

        new_room_name = str(request.POST.get('name'))
        new_room_capacity = int(request.POST.get('seats'))

        if new_room_name.isspace() or new_room_name == '':
            name_error = True

        if new_room_capacity <= 0:
            seats_error = True

        if request.POST.get('projector') == 'yes':
            has_projector = True

        if not name_error and not seats_error:
            room.name = new_room_name
            room.seats = new_room_capacity
            room.projector = has_projector
            room.save()
            is_room_updated = True

        return render(request, 'modify_room.html', {
            'room': room,
            'is_room_updated': is_room_updated,
            'name_error': name_error,
            'seats_error': seats_error,
        })


class NewBooking(View):
    def get(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)

        user_date = request.GET.get('date')

        if user_date != None:
            date = datetime.strptime(user_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            date = datetime.today().strftime("%Y-%m-%d")

        bookings = room.bookings.filter(date__gte=datetime.today())

        return render(request, 'new_booking.html', {
            'room': room,
            'date': date,
            'bookings': bookings,
        })

    def post(self, request, room_id):
        room_id = int(room_id)
        room = Room.objects.get(id=room_id)
        bookings = room.bookings.filter(date__gte=datetime.today())
        new_booking = []
        bookings_on_user_date = []
        date_is_past = False
        room_is_booked = False

        user_date = request.POST.get('date')
        date = datetime.strptime(user_date, '%Y-%m-%d').strftime('%Y-%m-%d')

        if date < datetime.today().strftime('%Y-%m-%d'):
            date = datetime.today().strftime('%Y-%m-%d')
            date_is_past = True
        else:
            date_is_past = False
            bookings_on_user_date = room.bookings.filter(date=user_date)

        if bookings_on_user_date:
            room_is_booked = True

        if not date_is_past and not room_is_booked:
            comment = request.POST.get('comment')
            new_booking = Booking.objects.create(room=room, comment=comment, date=request.POST.get('date'))

        return render(request, 'new_booking.html', {
            'room': room,
            'date': date,
            'date_is_past': date_is_past,
            'room_is_booked': room_is_booked,
            'new_booking': new_booking,
            'bookings': bookings,
        })
