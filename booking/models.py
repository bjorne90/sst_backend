from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from scheduling.models import WorkShift

User = get_user_model()


class Pass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    time = models.DateTimeField()
    role = models.CharField(max_length=100)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Pass #{self.id} - {self.user.username}"


class Booking(models.Model):
    workshift = models.ForeignKey('scheduling.WorkShift', on_delete=models.CASCADE, related_name='bookings')
    users = models.ManyToManyField(User, related_name='bookings')

    def __str__(self):
        return f"Booking: {', '.join([str(user) for user in self.users.all()])} - {self.workshift}"


class WorkShift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name
    


@receiver(post_save, sender=Booking)
def send_booking_email(sender, instance, created, **kwargs):
    if created:  # Check if a new booking record was created
        # Send an email to each user
        for user in instance.users.all():
            subject = 'Shift Booking Confirmation'
            message = 'You have been booked for a new shift.'
            email_from = settings.DEFAULT_FROM_EMAIL  # Replace with your own email
            recipient_list = [user.email]  # Send email to user

            html_message = render_to_string('email/booking_confirmation.html', {'booking': instance})
            send_mail(subject, message, email_from, recipient_list, html_message=html_message, fail_silently=False)