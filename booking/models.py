from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from scheduling.models import WorkShift
from booking.signals import booking_canceled

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
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking: {', '.join([str(user) for user in self.users.all()])} - {self.workshift}"


class WorkShift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    assigned_users = models.ManyToManyField(User, blank=True, related_name='assigned_shifts')

    def __str__(self):
        return self.name
    
@receiver(post_delete, sender=Booking)
def booking_deleted(sender, instance, **kwargs):
    # Trigger the booking_canceled signal when a booking is deleted
    booking_canceled.send(sender=instance)