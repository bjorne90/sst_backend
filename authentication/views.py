from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm
from scheduling.models import WorkShift
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                user_profile = user.profile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)

            # Send registration confirmation email
            send_registration_confirmation_email(user)

            return redirect(reverse('profiles:profile_detail'))
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})


def send_registration_confirmation_email(user):
    subject = 'Registration Confirmation'
    template_name = 'authentication/registration_email_template.html'
    context = {'username': user.username}
    html_message = render_to_string(template_name, context)
    recipient_list = [user.email]

    send_mail(subject, '', from_email=None, recipient_list=recipient_list, html_message=html_message)



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                user_profile = user.profile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=user)
            return redirect(reverse('profiles:profile_detail'))
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid login credentials'})
    return render(request, 'authentication/login.html')


def user_logout(request):
    logout(request)
    return redirect('authentication:login')

def user_login2(request):
    return render(request, 'authentication/login_registration.html')