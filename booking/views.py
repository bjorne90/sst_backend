from django.shortcuts import render, redirect, get_object_or_404
from .models import Pass
from datetime import datetime
from scheduling.models import WorkShift
from django import forms
from .models import Booking
from django.core.mail import EmailMessage

def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'booked_workshifts': bookings})



class PassForm(forms.Form):
    place = forms.CharField()
    time = forms.CharField()
    role = forms.CharField()

def book_pass(request, workshift_id):
    workshift = get_object_or_404(WorkShift, id=workshift_id)

    if not workshift.is_booked:
        new_pass, created = Pass.objects.get_or_create(user=request.user, workshift=workshift)

        if created:
            # Send email notification
            subject = 'Shift Booking Notification'
            message = f"You have successfully booked a shift.\n\nShift details:\nDate: {workshift.date}\nTime: {workshift.time}\nLocation: {workshift.location}"
            from_email = 'bjorn@pixaria.se'  # Replace with your email address
            to_email = request.user.email

            email = EmailMessage(subject, message, from_email, [to_email])
            email.send()

            return redirect('booking:booking_list')
        else:
            # Pass already exists, display an error message or redirect to a different page
            return redirect('scheduling:workshift_list')
    else:
        # Pass is already booked, display an error message or redirect to a different page
        return redirect('scheduling:workshift_list')
