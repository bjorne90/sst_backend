from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import WorkShift, Booking
from .views import send_email_notification


class WorkShiftModelTest(TestCase):
    def test_str_representation(self):
        workshift = WorkShift(event='Event Name')
        self.assertEqual(str(workshift), 'Event Name')


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workshift = WorkShift.objects.create(event='Event Name')
        self.booking = Booking.objects.create(user=self.user, workshift=self.workshift)

    def test_str_representation(self):
        expected_str = f"Booking: {self.user} - {self.workshift}"
        self.assertEqual(str(self.booking), expected_str)

    def test_save_method_adds_workshift_to_user_profile(self):
        self.assertTrue(self.workshift in self.user.profile.booked_workshifts.all())

    def test_save_method_sends_email_notification(self):
        with self.assertLogs('django', level='INFO') as logger:
            send_email_notification(self.workshift, self.user)

        self.assertEqual(len(logger.records), 1)
        self.assertEqual(logger.records[0].message, 'Email notification sent successfully.')


class WorkShiftListViewTest(TestCase):
    def test_workshift_list_view_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('scheduling:workshift_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/workshift_list.html')

    def test_workshift_list_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:workshift_list'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/workshift_list/')


class BookWorkshiftViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workshift = WorkShift.objects.create(event='Event Name', is_booked=False)

    def test_book_workshift_view_with_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('scheduling:book_workshift'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/book_workshift.html')

    def test_book_workshift_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:book_workshift'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/book_workshift/')

    def test_book_workshift_view_creates_booking(self):
        self.client.force_login(self.user)
        self.client.post(reverse('scheduling:book_workshift'), {'workshift_id': self.workshift.id})
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)
        self.assertEqual(Booking.objects.first().workshift, self.workshift)


class WorkShiftsViewTest(TestCase):
    def test_work_shifts_view_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('scheduling:work_shifts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/work_shifts.html')

    def test_work_shifts_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:work_shifts'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/work_shifts/')


class CancelWorkshiftViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.workshift = WorkShift.objects.create(event='Event Name', is_booked=True)
        self.user.profile.booked_workshifts.add(self.workshift)

    def test_cancel_workshift_view_with_logged_in_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('scheduling:cancel_workshift', args=[self.workshift.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/cancel_workshift.html')

    def test_cancel_workshift_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:cancel_workshift', args=[self.workshift.id]))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/cancel_workshift/1')

    def test_cancel_workshift_view_cancels_booking(self):
        self.client.force_login(self.user)
        self.client.post(reverse('scheduling:cancel_workshift', args=[self.workshift.id]))
        self.assertEqual(self.user.profile.booked_workshifts.count(), 0)
        self.assertFalse(Booking.objects.exists())
        self.assertFalse(self.workshift.is_booked)


class AddEventViewTest(TestCase):
    def test_add_event_view_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('scheduling:add_event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/add_event.html')

    def test_add_event_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:add_event'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/add_event/')


class CalendarViewTest(TestCase):
    def test_calendar_view_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('scheduling:calendar_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/calendar2.html')

    def test_calendar_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:calendar_view'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/calendar_view/')


class EmployeesCalendarViewTest(TestCase):
    def test_employees_calendar_view_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(user)
        response = self.client.get(reverse('scheduling:employees_calendar_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scheduling/employees_calendar.html')

    def test_employees_calendar_view_redirects_when_user_not_logged_in(self):
        response = self.client.get(reverse('scheduling:employees_calendar_view'))
        self.assertRedirects(response, '/accounts/login/?next=/scheduling/employees_calendar_view/')
