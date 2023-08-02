from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from scheduling.models import WorkShift
from django.core.validators import MaxLengthValidator

def upload_to(instance, filename):
    return f'profile_images/{instance.user.username}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    about_me = models.TextField(validators=[MaxLengthValidator(400)], blank=True)
    phone_number = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=200, default='')
    booked_workshifts = models.ManyToManyField(WorkShift, related_name='booked_by')
    work_title = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to=upload_to, blank=True, null=True, default='default_profile_image.png')
    work_id = models.CharField(max_length=200, default='')
    ov_id = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
