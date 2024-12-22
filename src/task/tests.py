from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .form import postTask
from datetime import datetime, timedelta

class PostTaskTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_post_task_get_request(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('tasks:postTask'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/postTask.html')

    def test_post_task_valid_data(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'New Task',
            'taskDescription': 'This is a new task.',
            'category': 'tutoring',
            'location': 'Test Location',
            'budget': 100.00,
            'deadline': datetime.now() + timedelta(days=5),
            'disability': 'No'
        }
        response = self.client.post(reverse('tasks:postTask'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.title, 'New Task')
        self.assertEqual(task.owner, self.user)

    def test_post_task_invalid_data(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': '',  # Missing required fields
            'taskDescription': '',
        }
        response = self.client.post(reverse('tasks:postTask'), data)
        self.assertEqual(response.status_code, 200)  # Form error keeps the user on the same page
        self.assertContains(response, 'This field is required.')  # Check for form errors in response
