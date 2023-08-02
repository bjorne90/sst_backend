from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm

class ProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_detail_view(self):
        url = reverse('profiles:profile_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    def test_edit_profile_view(self):
        url = reverse('profiles:edit_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/edit_profile.html')

    def test_edit_profile_view_post(self):
        url = reverse('profiles:edit_profile')
        form_data = {
            'phone_number': '1234567890',
            'email': 'test@example.com',
            'about_me': 'Test about me',
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertRedirects(response, reverse('profiles:profile_detail'))

        # Check if the profile is updated with the new data
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone_number, form_data['phone_number'])
        self.assertEqual(self.profile.user.email, form_data['email'])
        self.assertEqual(self.profile.about_me, form_data['about_me'])

    def test_user_login_view(self):
        url = reverse('profiles:user_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to profile detail page
        self.assertRedirects(response, reverse('profiles:profile_detail'))

    def test_profile_view(self):
        url = reverse('profiles:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_work_shifts_view(self):
        url = reverse('profiles:work_shifts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

    def test_links_view(self):
        url = reverse('profiles:links')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/links.html')

    def test_knowledge_base_view(self):
        url = reverse('profiles:knowledge_base')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/knowledgebase.html')

    def test_employees_view(self):
        url = reverse('profiles:employees')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'employees.html')

    def test_admin_view_profiles_view(self):
        url = reverse('profiles:admin_view_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/admin_view_profiles.html')
