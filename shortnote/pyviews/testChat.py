import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shortnote.models import UserProfile, Chat
import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')

# Setup Django
django.setup()


class TestChatFunctions(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.friend = User.objects.create_user(
            username='testfriend', password='12345'
        )
        self.friend_profile = UserProfile.objects.create(user=self.friend)
        self.user_profile.friends.add(self.friend_profile)
        self.client.login(username='testuser', password='12345')

    def test_load_chat(self):
        # Create some test chat messages
        Chat.objects.create(
            sender=self.user,
            receiver=self.friend,
            content='Hello'
        )
        Chat.objects.create(
            sender=self.friend,
            receiver=self.user,
            content='Hi there'
        )

        response = self.client.get(reverse('load_chat'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['chats']), 2)
        self.assertEqual(data['chats'][0]['content'], 'Hello')
        self.assertEqual(data['chats'][1]['content'], 'Hi there')

    def test_send_chat(self):
        response = self.client.post(reverse('send_chat'), {
            'content': 'Test message',
            'receiver': self.friend.username
        })
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data['success'])

        # Check if the message was actually saved in the database
        chat = Chat.objects.last()
        self.assertEqual(chat.content, 'Test message')
        self.assertEqual(chat.sender, self.user)
        self.assertEqual(chat.receiver, self.friend)

    def test_send_chat_invalid_receiver(self):
        response = self.client.post(reverse('send_chat'), {
            'content': 'Test message',
            'receiver': 'nonexistent_user'
        })
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Invalid receiver')

    def test_load_chat_no_messages(self):
        response = self.client.get(reverse('load_chat'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['chats']), 0)


if __name__ == '__main__':
    unittest.main()
