from django import forms
from django.contrib import admin
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['work_id', 'phone_number', 'address', 'profile_image', 'booked_workshifts', 'ov_id']
        widgets = {
            'booked_workshifts': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booked_workshifts'].required = False


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    filter_horizontal = ('booked_workshifts',)


admin.site.register(Profile, ProfileAdmin)
