from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch









if __name__ == '__main__':
    TestCase.main()
    
class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("user:signup")  
    @patch("user.views.send_mail")  
    def test_successful_signup(self, mock_send_mail):
        # Mock send_mail to avoid sending emails during testing
        mock_send_mail.return_value = 1
        
        response = self.client.post(self.signup_url, {
            "UserName": "testuser",
            "email": "test@example.com",
            "password": "strongpassword",
            "confirm_password": "strongpassword"
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect to OTP verification page.
        self.assertEqual(response.url, reverse("user:verify_email"))
        self.assertTrue(User.objects.filter(username="testuser").exists())

        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("strongpassword"))

    def test_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            "UserName": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password456"
        })

        self.assertEqual(response.status_code, 200)  # Renders signup template again.
        self.assertContains(response, "Passwords do not match.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_password_too_short(self):
        response = self.client.post(self.signup_url, {
            "UserName": "testuser",
            "email": "test@example.com",
            "password": "short",
            "confirm_password": "short"
        })

        self.assertEqual(response.status_code, 200)  # Renders signup template again.
        self.assertContains(response, "Password must be at least 8 characters.")
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_username_already_taken(self):
        User.objects.create_user(username="testuser", email="another@example.com", password="password123")
        
        response = self.client.post(self.signup_url, {
            "UserName": "testuser",
            "email": "test@example.com",
            "password": "strongpassword",
            "confirm_password": "strongpassword"
        })

        self.assertEqual(response.status_code, 200)  # Renders signup template again.
        self.assertContains(response, "Username is already taken.")
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)

    def test_email_already_registered(self):
        User.objects.create_user(username="anotheruser", email="test@example.com", password="password123")
        
        response = self.client.post(self.signup_url, {
            "UserName": "testuser",
            "email": "test@example.com",
            "password": "strongpassword",
            "confirm_password": "strongpassword"
        })

        self.assertEqual(response.status_code, 200)  # Renders signup template again.
        self.assertContains(response, "Email is already registered.")
        self.assertEqual(User.objects.filter(email="test@example.com").count(), 1)
