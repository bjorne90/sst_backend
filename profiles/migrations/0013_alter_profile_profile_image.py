# Generated by Django 3.2.19 on 2023-05-10 22:29

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_profile_work_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile_image.png', null=True, upload_to=profiles.models.upload_to),
        ),
    ]