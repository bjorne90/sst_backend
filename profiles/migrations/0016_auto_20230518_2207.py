# Generated by Django 3.2.18 on 2023-05-18 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0015_document'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AddField(
            model_name='profile',
            name='work_id',
            field=models.CharField(default='', max_length=200),
        ),
    ]