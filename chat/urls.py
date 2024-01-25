from django.urls import path, include

from . import views

urlpatterns = [
    # API endpoints
    path('', views.index, name='index'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('messages/', views.get_all_messages, name='message_data'),
    path('rooms/', views.get_all_rooms, name='all_rooms_data'),
    path('rooms/<str:room_name>/', views.get_room_data, name='single_room_data'),
    
    # Template views
    path('<str:room_name>/', views.room, name='room'),
]
