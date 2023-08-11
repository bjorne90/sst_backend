from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pass
from datetime import datetime
from scheduling.models import WorkShift
from django import forms
from .models import Booking
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import BookingSerializer
from rest_framework import viewsets

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# Define the email sending function
def send_email_notification(workshift, user, recipient_list, template_path, subject):
    message = render_to_string(template_path, {'workshift': workshift})
    html_message = render_to_string(template_path, {'workshift': workshift})

    send_mail(subject, message, from_email=None, recipient_list=recipient_list, html_message=html_message)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_booking_list(request):
    bookings = Booking.objects.filter(users=request.user)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

def booking_list(request):
    bookings = Booking.objects.filter(users=request.user)
    return render(request, 'booking/booking_list.html', {'booked_workshifts': bookings})

class PassForm(forms.Form):
    place = forms.CharField()
    time = forms.CharField()
    role = forms.CharField()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_approved_booking_list(request):
    approved_bookings = Booking.objects.filter(user=request.user, is_approved=True)
    serializer = BookingSerializer(approved_bookings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_pass(request, workshift_id):
    workshift = get_object_or_404(WorkShift, id=workshift_id)
    print("Is booked:", workshift.is_booked)

    new_pass, created = Pass.objects.get_or_create(user=request.user, workshift=workshift)
    print("Created:", created)

    if created:
        
        # Send notification email to admin
        subject_admin = 'En bokning behöver godkännas'
        template_path_admin = 'scheduling/email_template_admin.html'
        recipient_list_admin = ['noreplay@pixaria.se']  # Admin's email address
        message_admin = f"A new shift booking requires your approval.\n\nUser: {request.user}\nShift: {workshift}"
        send_mail(subject_admin, message_admin, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=recipient_list_admin)

        return Response({'detail': 'You have successfully booked the workshift, pending admin approval.'}, status=status.HTTP_201_CREATED)
    else:
        # Pass already exists, display an error message or redirect to a different page
        return Response({'detail': 'Shift booking failed.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])  # Create a new API view for admin approval
@permission_classes([IsAdminUser])  # Only admin can approve bookings
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Perform any additional validation or logic for approval here
    booking.is_approved = True
    booking.save()

    # Notify the user that their booking has been approved
    send_email_notification_booking_approved(booking)  # Implement this function to send email

    return Response({'detail': 'Booking approved successfully.'}, status=status.HTTP_200_OK)

def send_email_notification_booking_approved(booking):
    subject_user = 'Ditt pass är godkännt'
    template_path_user = 'booking/email_template_booking_approved.html'
    recipient_list_user = [booking.user.email]
    send_email_notification(booking.workshift, booking.user, recipient_list_user, template_path_user, subject_user)

