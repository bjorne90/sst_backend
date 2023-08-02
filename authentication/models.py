from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import Booking

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_profile')
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    booked_workshifts = models.ManyToManyField(Booking, related_name='booked_users')

    def __str__(self):
        return self.user.username
