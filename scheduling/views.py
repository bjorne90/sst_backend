from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import WorkShift
from profiles.models import Profile
from .serializers import WorkShiftSerializer
from booking.models import Booking
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated


class WorkShiftListCreateView(generics.ListCreateAPIView):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.profile
        print(self.request.user)  # Log the user
        print(user_profile)      # Log the profile associated with the user
        now = timezone.now()
        return user_profile.booked_workshifts.filter(start_time__gt=now)

class BookWorkShiftView(generics.CreateAPIView):
    queryset = WorkShift.objects.filter(is_booked=False)
    serializer_class = WorkShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        selected_workshift_id = request.data.get('workshift_id')
        selected_workshift = get_object_or_404(WorkShift, id=selected_workshift_id)

        # Check if the selected workshift is already booked
        if selected_workshift.is_booked:
            return Response({'detail': 'This workshift has already been booked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the workshift has already passed
        current_datetime = timezone.now()
        if selected_workshift.start_time < current_datetime:
            return Response({'detail': 'This workshift has already passed and cannot be booked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new booking object
        booking = Booking.objects.create(user=request.user, workshift=selected_workshift)

        # Update the user's profile with the booked workshift
        user_profile = request.user.profile
        user_profile.booked_workshifts.add(selected_workshift)
        user_profile.save()

        # Update the availability of the workshift
        selected_workshift.is_booked = True
        selected_workshift.save()

        # Send booking confirmation email
        send_email_notification(selected_workshift, request.user)

        return Response({'detail': 'You have successfully booked the workshift.'}, status=status.HTTP_201_CREATED)

class CancelWorkShiftView(generics.UpdateAPIView):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        workshift = self.get_object()

        # Check if the workshift is already booked
        if not workshift.is_booked:
            return Response({'detail': 'This workshift is not booked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current user's profile
        user_profile = request.user.profile

        # Check if the user has booked the workshift
        if workshift not in user_profile.booked_workshifts.all():
            return Response({'detail': 'You have not booked this workshift.'}, status=status.HTTP_400_BAD_REQUEST)

        # Remove the workshift from the user's booked workshifts
        user_profile.booked_workshifts.remove(workshift)
        user_profile.save()

        # Update the availability of the workshift
        workshift.is_booked = False
        workshift.save()

        return Response({'detail': 'Workshift canceled successfully.'}, status=status.HTTP_200_OK)

def send_email_notification(workshift, user):
    subject = 'Workshift Booking Confirmation'
    message = render_to_string('scheduling/email_template.html', {'workshift': workshift})
    recipient_list = [user.email]
    html_message = render_to_string('scheduling/email_template.html', {'workshift': workshift})

    send_mail(subject, message, from_email=None, recipient_list=recipient_list, html_message=html_message)
