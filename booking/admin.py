from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models

from .models import Booking

User = get_user_model()


class BookingAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(verbose_name='Users', is_stacked=False)},
    }
    filter_horizontal = ('users',)


admin.site.register(Booking, BookingAdmin)
