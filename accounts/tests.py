from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsViewTest(TestCase):
    """Tests for accounts app views"""

    def setUp(self):
        self.client = Client()

    def test_signup_page_loads(self):
        """Test that signup page loads successfully"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_successful_signup(self):
        """Test that a user can sign up successfully"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        })
        # Should redirect to login page after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_with_mismatched_passwords(self):
        """Test that signup fails with mismatched passwords"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'TestPassword123!',
            'password2': 'DifferentPassword123!',
        })
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_successful_login(self):
        """Test that a user can log in successfully"""
        # Create a user
        User.objects.create_user(username='testuser', password='testpass123')

        # Attempt to log in
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })

        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        # User should be authenticated
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_login_with_wrong_password(self):
        """Test that login fails with wrong password"""
        # Create a user
        User.objects.create_user(username='testuser', password='testpass123')

        # Attempt to log in with wrong password
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })

        # Should stay on login page
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test that a user can log out"""
        # Create and log in a user
        User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        # Log out
        response = self.client.post(reverse('logout'))

        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))