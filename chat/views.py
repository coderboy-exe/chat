import json
from django.shortcuts import render
from django.http import HttpResponseForbidden 
from django.http import JsonResponse as Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt

from .models import UserModel, Message, Room
from core import settings

# Create your views here.

def index(request):
    user = request.user
    context = {
       "user":user,
       "error": ""
   }
    return render(request, 'index.html', context=context)

def room(request, room_name, **kwargs):
    """_summary_

    Args:
        request (_type_): _description_
        room_name (str): room name

    Returns:
        view: returns a view template
    """
    api_key = request.GET.get('api_key')
    if api_key != settings.API_KEY:
        return render(request, 'index.html', {'error': 'Invalid API key'})
    
    context = {
        "room_name": room_name,
    }
   
    return render(request, 'chatroom.html', {"room_name": room_name})


def get_room_data(request, room_name):
    """_summary_

    Args:
        request (_type_): _description_
        room_name (str): name of the room

    Returns:
        list: room details
    """
    api_key = request.GET.get('api_key')
    if api_key != settings.API_KEY:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    room_data = Room.objects.filter(name=f"chat_{room_name}")
    serialized_data = serialize('json', room_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)


def get_all_rooms(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        list: list of all rooms
    """
    api_key = request.GET.get('api_key')
    if api_key != settings.API_KEY:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    room_data = Room.objects.all()
    serialized_data = serialize('json', room_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)


def get_all_messages(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        list: list of all messages
    """
    api_key = request.GET.get('api_key')
    if api_key != settings.API_KEY:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    room_id = request.GET.get('room_id')
    if room_id:
        message_data = Message.objects.filter(room=room_id)
    else:
        message_data = Message.objects.all()
    serialized_data = serialize('json', message_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)


    


@csrf_exempt
def mark_as_read(request, message_id):
    """_summary_

    Args:
        request (_type_): _description_
        message_id (int): id of the message to be marked as "read"

    Returns:
        dict: {"status": "]"}
    """
    api_key = request.GET.get('api_key')
    if api_key != settings.API_KEY:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)