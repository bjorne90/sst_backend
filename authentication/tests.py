from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserRegistrationForm


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='Test Address'
        )

    def test_user_profile_creation(self):
        self.assertEqual(str(self.profile), self.user.username)

    def test_user_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_existing_email(self):
        form_data = {
            'username': 'existinguser',
            'email': 'test@example.com',  # Existing email from the setup
            'first_name': 'Existing',
            'last_name': 'User',
            'password1': 'existingpassword',
            'password2': 'existingpassword',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'Email is already in use.')


class UserProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_register_view(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_register_view_post(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post('/register/', data=form_data)
        self.assertRedirects(response, '/profiles/profile_detail/')

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_view_post(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/login/', data=form_data)
        self.assertRedirects(response, '/profiles/profile_detail/')

    def test_logout_view(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

    def test_login2_view(self):
        response = self.client.get('/login2/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login_registration.html')
