import uuid
from django.test import TestCase
from django.urls import reverse

# Create your tests here.

from .models import Room, Message, UserModel
from django.contrib.auth.models import User

class ChatViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = UserModel.objects.create(id=str(uuid.uuid4()))

        # Create a room for testing
        self.room = Room.objects.create(name='test_room')

        # Create a message for testing
        self.message = Message.objects.create(sender=self.user.id, content='Test message', room=self.room)
        
        # Set valid API key
        self.expected_api_key = "my_api_key"

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_room_view_invalid_or_no_api_key(self):
        response = self.client.get(reverse('room', kwargs={'room_name': 'test_room'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['error'], 'Invalid API key')
    
    def test_room_view_valid_api_key(self):
        # Valid API key
        expected_api_key = "my_api_key"
        url = reverse('room', kwargs={'room_name': 'test_room'}) + f'?api_key={expected_api_key}'
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatroom.html')
        self.assertEqual(response.context['room_name'], 'test_room')

    def test_get_room_data(self):
        # Valid API key
        expected_api_key = "my_api_key"
        url = reverse('single_room_data', kwargs={'room_name': 'test_room'}) + f'?api_key={expected_api_key}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
    def test_get_room_data_invalid_api_key(self):
        # Set invalid API key
        invalid_api_key = "invalid_key"
        url = reverse('single_room_data', kwargs={'room_name': 'test_room'}) + f'?api_key={invalid_api_key}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid API key')   

    def test_get_all_rooms(self):
        # Valid API key
        expected_api_key = "my_api_key"
        url = reverse('all_rooms_data') + f'?api_key={expected_api_key}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('fields', response.json()[0])
        
    def test_get_all_messages(self):
        # Valid API key
        expected_api_key = "my_api_key"
        url = reverse('message_data') + f'?api_key={expected_api_key}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('fields', response.json()[0])
        
    def test_mark_as_read(self):
        # Valid API key
        expected_api_key = "my_api_key"
        url = reverse('mark_as_read', kwargs={'message_id': self.message.pk}) + f'?api_key={expected_api_key}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)

