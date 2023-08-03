from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address', 'work_title']  # fields to be displayed in the list view
    search_fields = ['user__username', 'phone_number', 'work_title']  # fields to be searched in the search bar
    filter_horizontal = ('booked_workshifts',)

admin.site.register(Profile, ProfileAdmin)
