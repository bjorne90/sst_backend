from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import WorkShift, Booking
from scheduling.views import send_email_notification
from django.contrib.admin.widgets import AdminSplitDateTime

class CustomSplitDateTimeWidget(AdminSplitDateTime):
    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 1

class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('event', 'formatted_start_time', 'formatted_end_time', 'is_booked', 'role')
    list_display_links = ('event',)
    inlines = [BookingInline]

    def formatted_start_time(self, obj):
        return obj.start_time.strftime('%Y-%m-%d %H:%M')

    def formatted_end_time(self, obj):
        return obj.end_time.strftime('%Y-%m-%d %H:%M')

    formatted_start_time.short_description = 'Start Time'
    formatted_end_time.short_description = 'End Time'

    def assign_user(self, request, queryset):
        for workshift in queryset:
            if not workshift.is_booked:
                # Retrieve all users
                users = User.objects.all()

                # Create a new booking object for each user
                for user in users:
                    booking = Booking.objects.create(user=user, workshift=workshift)
                    send_email_notification(workshift, user)

                # Update the availability of the workshift
                workshift.is_booked = True
                workshift.save()

    assign_user.short_description = "Assign users to selected workshifts"

    formfield_overrides = {
    models.DateTimeField: {'widget': CustomSplitDateTimeWidget},
}

admin.site.register(WorkShift, WorkShiftAdmin)
