from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import WorkShift
from profiles.models import Profile
from .forms import EventForm
from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from .models import Booking


@login_required
def workshift_list(request):
    user_profile = request.user.profile
    now = timezone.now()
    booked_workshifts = user_profile.booked_workshifts.filter(start_time__gt=now)
    return render(request, 'scheduling/workshift_list.html', {'booked_workshifts': booked_workshifts})


@login_required
def book_workshift(request):
    workshifts = WorkShift.objects.filter(is_booked=False)

    if request.method == 'POST':
        # Handle the booking logic
        # ...

        # Check if the selected workshift is already booked
        selected_workshift_id = request.POST.get('workshift_id')
        selected_workshift = get_object_or_404(WorkShift, id=selected_workshift_id)
        if selected_workshift.is_booked:
            messages.error(request, 'This workshift has already been booked.')
            return redirect('scheduling:book_workshift')

        # Check if the workshift has already passed
        current_datetime = timezone.now()
        if selected_workshift.start_time < timezone.now():
            error_message = 'This workshift has already passed and cannot be booked.'
            return render(request, 'scheduling/book_workshift.html', {'workshifts': workshifts, 'error_message': error_message})

        # Create a new booking object
        booking = Booking.objects.create(user=request.user, workshift=selected_workshift)

        # Update the user's profile with the booked workshift
        user_profile = request.user.profile
        user_profile.booked_workshifts.add(selected_workshift)
        user_profile.save()

        # Update the availability of the workshift
        selected_workshift.is_booked = True
        selected_workshift.save()

        # Render the email template
        email_template = send_email_notification(selected_workshift, request.user)

        # Render a success message
        success_message = 'You have successfully booked the workshift.'
        return render(request, 'scheduling/book_workshift.html', {'success_message': success_message, 'email_template': email_template})

    return render(request, 'scheduling/book_workshift.html', {'workshifts': workshifts})




@login_required
def work_shifts(request):
    user_profile = request.user.profile
    now = timezone.now()
    booked_workshifts = user_profile.booked_workshifts.filter(start_time__gt=now)
    worked_workshifts = user_profile.booked_workshifts.filter(start_time__lte=now)
    return render(request, 'scheduling/work_shifts.html', {'booked_workshifts': booked_workshifts, 'worked_workshifts': worked_workshifts})


@login_required
def cancel_workshift(request, workshift_id):
    workshift = get_object_or_404(WorkShift, id=workshift_id)

    if request.method == 'POST':
        # Check if the workshift is already booked
        if not workshift.is_booked:
            messages.error(request, f'{workshift.booked_by.first().user.first_name} {workshift.booked_by.first().user.last_name} wants to cancel the workshift "{workshift.event}".')
            return redirect('scheduling:work_shifts')

        # Get the current user's profile
        user_profile = request.user.profile

        # Check if the user has booked the workshift
        if workshift not in user_profile.booked_workshifts.all():
            messages.error(request, 'You have not booked this workshift.')
            return redirect('scheduling:work_shifts')

        # Remove the workshift from the user's booked workshifts
        user_profile.booked_workshifts.remove(workshift)

        # Update the availability of the workshift
        workshift.is_booked = False
        workshift.save()

        messages.success(request, 'Workshift canceled successfully.')
        return redirect('scheduling:work_shifts')

    # Handle GET request (show confirmation page)
    return render(request, 'scheduling/cancel_workshift.html', {'workshift': workshift})



def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scheduling:work_shifts')
    else:
        form = EventForm()
    return render(request, 'scheduling/add_event.html', {'form': form})

def calendar_view(request):
    shifts = WorkShift.objects.filter(is_booked=False)
    return render(request, 'scheduling/calendar2.html', {'shifts': shifts})

def employees_calendar_view(request):
    shifts = WorkShift.objects.filter(is_booked=True)
    all_shifts = WorkShift.objects.all()  # or any other query you want to use
    return render(request, 'scheduling/employees_calendar.html', {'shifts': shifts, 'all_shifts': all_shifts})


def send_email_notification(workshift, user):
    subject = 'Workshift Booking Confirmation'
    message = render_to_string('scheduling/email_template.html', {'workshift': workshift})
    recipient_list = [user.email]
    html_message = render_to_string('scheduling/email_template.html', {'workshift': workshift})

    send_mail(subject, message, from_email=None, recipient_list=recipient_list, html_message=html_message)
    pass