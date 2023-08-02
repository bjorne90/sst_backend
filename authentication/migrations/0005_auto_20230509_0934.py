# Generated by Django 3.2.19 on 2023-05-09 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0003_alter_workshift_name'),
        ('authentication', '0004_remove_userprofile_booked_workshifts'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='booked_workshifts',
            field=models.ManyToManyField(related_name='booked_users', to='booking.Booking'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authentication_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
