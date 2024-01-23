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

# Create your views here.

def index(request):
    user = request.user
    context = {
       "user":user
   }
    return render(request, 'index.html', context=context)

def room(request, room_name, **kwargs):
    # return Response({"room_name": room_name})
    # gp = Group.objects.create(room=room_name, members=request.user)
    context = {
        "room_name": room_name,
    }
   
    return render(request, 'chatroom.html', {"room_name": room_name})


def get_room_data(request, room_name):
    room_data = Room.objects.filter(name=rf"chat_{room_name}")
    serialized_data = serialize('json', room_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)


def get_all_rooms(request):
    room_data = Room.objects.all()
    serialized_data = serialize('json', room_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)

def get_all_messages(request):
    message_data = Message.objects.all()
    serialized_data = serialize('json', message_data)
    return JsonResponse(json.loads(serialized_data), safe=False, status=200)


@csrf_exempt
def mark_as_read(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return JsonResponse({'status': 'success'})
    except Message.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found'}, status=404)