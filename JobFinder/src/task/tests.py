from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Apply
from .form import postTask
from datetime import datetime, timedelta
from django.utils.text import slugify
from django.utils import timezone
from django.db import transaction
from django.db import IntegrityError, transaction

class PostTaskViewTest(TestCase):
    def setUp(self):
        """Set up for each test."""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.post_url = reverse('tasks:postTask')
        self.deadline = timezone.now() + timedelta(days=10)

    def test_get_request_renders_form(self):
        """Ensure the form is rendered on a GET request."""
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/postTask.html')
        self.assertIsInstance(response.context['form'], postTask)

    def test_post_request_valid_form(self):
        """Ensure a task is created with valid data."""
        data = {
            'title': 'Test Task',
            'taskDescription': 'This is a test task description.',
            'category': 'home_repair',
            'location': '123 Main Street',
            'budget': '50.00',
            'deadline': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        response = self.client.post(self.post_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Task.objects.filter(owner=self.user, title='Test Task').exists())

    def test_post_request_invalid_form(self):
        """Ensure invalid data does not create a task."""
        data = {
            'title': '',  # Empty title should trigger validation error
            'taskDescription': 'This is a test task description.',
            'category': 'home_repair',
            'location': '123 Orabi Street',
            'budget': '50.00',
            'deadline': '',
        }
        response = self.client.post(self.post_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.exists())  # Task should not be created
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_task_saved_with_correct_data(self):
        """Ensure the task is saved with the correct data."""
        data = {
            'title': 'Correct Task',
            'taskDescription': 'Details of the task.',
            'category': 'delivery',
            'location': 'Another Street',
            'budget': '100.00',
            'deadline': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
        }
        response = self.client.post(self.post_url, data)
        task = Task.objects.get(title='Correct Task')
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.category, 'delivery')
        self.assertEqual(float(task.budget), 100.00)

    def test_unauthenticated_user_redirected(self):
        """Ensure unauthenticated users are redirected to the login page."""
        self.client.logout()  # Log out the user
        response = self.client.get(self.post_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/user/login/?next={self.post_url}')

def test_task_slug_is_generated(self):
        """Ensure a slug is generated for each task."""
        try:
            with transaction.atomic():  # Ensure atomic transaction
                task = Task(
                    title="Slug Test Task",
                    owner=self.user,
                    taskDescription="Test description",
                    deadline=self.deadline
                )
                
                # Save the task explicitly
                task.save(force_insert=True)
                
                # Assert that slug is generated correctly
                self.assertIsNotNone(task.slug)
                expected_slug = f"{slugify(task.title)}-{task.id}"
                self.assertEqual(task.slug, expected_slug)

        except IntegrityError as e:
            self.fail(f"Test failed due to unexpected database integrity error: {e}")
        except Exception as e:
            self.fail(f"Test failed due to unexpected error: {e}")


def test_task_with_applicants(self):
    """Ensure tasks can correctly associate applicants."""
    try:
        with transaction.atomic(): 
            data = {
                'title': 'Applicant Task',
                'taskDescription': 'Task with applicants.',
                'category': 'tutoring',
                'location': '',
                'budget': '150.00',
                'deadline': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
            }
            self.client.post(self.post_url, data)
            task = Task.objects.get(title='Applicant Task')
            applicant = User.objects.create_user(username='applicant', password='password')
            Apply.objects.create(task=task, applicant=applicant)
            self.assertEqual(task.applications.count(), 1)
            self.assertEqual(task.applications.first().applicant.username, 'applicant')
    except Exception as e:
        self.fail(f"Test failed due to unexpected error: {e}")

