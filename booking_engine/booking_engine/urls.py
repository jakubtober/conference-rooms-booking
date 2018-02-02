"""booking_engine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from book_conference.views import Rooms, NewRoom, RoomDetails, NewBooking, DeleteRoom, ModifyRoom

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rooms/', Rooms.as_view(), name='rooms'),
    url(r'^room/new/', NewRoom.as_view(), name='new_room'),
    url(r'^room/delete/(?P<room_id>\d+)/', DeleteRoom.as_view(), name='delete_room'),
    url(r'^room/modify/(?P<room_id>\d+)/', ModifyRoom.as_view(), name='modify_room'),
    url(r'^room/(?P<room_id>\d+)/', RoomDetails.as_view(), name='details'),
    url(r'^reservation/(?P<room_id>\d+)/', NewBooking.as_view(), name='reservation'),
]
