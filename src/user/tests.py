from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from user.models import Profile


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse("user:signup")  # Replace "user:signup" with your actual signup view URL name.

    @patch("user.views.send_mail")  # Mock send_mail to avoid actually sending emails
    def test_signup_success(self, mock_send_mail):
        # Valid input data
        data = {
            "UserName": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was created
        user = User.objects.filter(username="testuser").first()
        self.assertIsNotNone(user)

        # Check that a profile was created for the user
        profile = Profile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)

        # Check that OTP email was sent
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(mock_send_mail.call_count, 1)

        # Check that the email was saved in the session
        self.assertEqual(self.client.session["email"], "testuser@example.com")

        # Check that the user is redirected to the OTP verification page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:verify_email"))  # Replace with the actual URL name.

    def test_signup_password_mismatch(self):
        # Invalid input: Passwords do not match
        data = {
            "UserName": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "confirm_password": "wrongpassword",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was not created
        user = User.objects.filter(username="testuser").first()
        self.assertIsNone(user)

        # Check that the error message is rendered
        self.assertContains(response, "Passwords do not match.")

    def test_signup_username_already_taken(self):
        # Create a user to simulate username conflict
        User.objects.create_user(username="testuser", email="existing@example.com", password="securepassword123")

        data = {
            "UserName": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was not created
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)

        # Check that the error message is rendered
        self.assertContains(response, "Username is already taken.")

    def test_signup_email_already_registered(self):
        # Create a user to simulate email conflict
        User.objects.create_user(username="existinguser", email="testuser@example.com", password="securepassword123")

        data = {
            "UserName": "newuser",
            "email": "testuser@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was not created
        self.assertEqual(User.objects.filter(username="newuser").count(), 0)

        # Check that the error message is rendered
        self.assertContains(response, "Email is already registered.")
    def test_signup_weak_password(self):
        data = {
            "UserName": "weakpassworduser",
            "email": "weakpassword@example.com",
            "password": "12345",
            "confirm_password": "12345",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was not created
        user = User.objects.filter(username="weakpassworduser").first()
        self.assertIsNone(user)

        # Check that the error message is rendered
        self.assertContains(response, "Password must be at least 8 characters.")

    
    def test_signup_missing_confirm_password(self):
        data = {
            "UserName": "noconfirmpassword",
            "email": "noconfirmpassword@example.com",
            "password": "securepassword123",
            "confirm_password": "",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was not created
        user = User.objects.filter(username="noconfirmpassword").first()
        self.assertIsNone(user)

        # Check that the error message is rendered
        self.assertContains(response, "Passwords do not match.", status_code=200)



    def test_signup_get_request(self):
        response = self.client.get(self.signup_url)

        # Check that the user was not created
        self.assertEqual(User.objects.count(), 0)

        # Check that the signup page is rendered
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    @patch("user.views.send_mail")
    def test_signup_email_in_session(self, mock_send_mail):
        data = {
            "UserName": "sessionuser",
            "email": "sessionuser@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
        }

        self.client.post(self.signup_url, data)

        # Check that the email is stored in the session
        self.assertIn("email", self.client.session)
        self.assertEqual(self.client.session["email"], "sessionuser@example.com")
    @patch("user.views.send_mail")
    def test_signup_with_extra_fields(self, mock_send_mail):
        data = {
            "UserName": "extrafielduser",
            "email": "extrafield@example.com",
            "password": "securepassword123",
            "confirm_password": "securepassword123",
            "extra_field": "unexpected_value",
        }

        response = self.client.post(self.signup_url, data)

        # Check that the user was created
        user = User.objects.filter(username="extrafielduser").first()
        self.assertIsNotNone(user)

        # Check that the user is redirected to the OTP verification page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:verify_email"))



