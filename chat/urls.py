from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('api/messages/', views.get_all_messages, name='message_data'),
    path('api/rooms/', views.get_all_rooms, name='room_data'),
    path('api/rooms/<str:room_name>/', views.get_room_data, name='room_data'),
    path('<str:room_name>/', views.room, name='room'),
]
