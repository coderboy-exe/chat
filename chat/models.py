from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from uuid import uuid4
from datetime import datetime

from django.urls import reverse
# Create your models here.

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(UserModel, related_name='rooms', blank=True)

    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    room = models.ForeignKey(Room, related_name="rooms", on_delete=models.CASCADE)
    sender = models.UUIDField()
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)
    