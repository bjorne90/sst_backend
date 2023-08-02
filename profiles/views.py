from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse
from .models import Profile
from booking.models import Booking
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def profile_detail(request):
    try:
        profile = Profile.objects.get(user=request.user)
        booked_workshifts = profile.booked_workshifts.all()
        
        next_workshift = None
        for booked_workshift in booked_workshifts.order_by('start_time'):
            if booked_workshift.start_time > timezone.now():
                next_workshift = booked_workshift
                break

        context = {
            'profile': profile,
            'next_workshift': next_workshift,
        }

        return render(request, 'profiles/profile_detail.html', context)
    except Profile.DoesNotExist:
        return render(request, 'profiles/create_profile.html')


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Update the profile with the form data
        profile.phone_number = request.POST.get('phone_number')
        profile.email = request.POST.get('email')
        profile.about_me = request.POST.get('about_me')
        profile.profile_image = request.FILES.get('profile_image')

        # Check if the password field is not empty
        password = request.POST.get('password')
        if password:
            confirm_password = request.POST.get('confirm_password')
            # Check if the password and confirm_password match
            if password == confirm_password:
                # Update the user's password
                profile.user.set_password(password)
                profile.user.save()
            else:
                return render(request, 'profiles/edit_profile.html', {'profile': profile, 'error': 'Passwords do not match'})

        # Save the updated profile
        profile.save()

        # Redirect to the profile detail page
        return redirect('profiles:profile_detail')
    else:
        return render(request, 'profiles/edit_profile.html', {'profile': profile})



def user_login(request):
    # Login logic
    # ...

    return redirect(reverse('profiles:profile_detail'))

@login_required
def profile(request):
    user_profile = request.user.profile
    booked_workshifts = user_profile.booked_workshifts.all()
    return render(request, 'profiles/profile.html', {'booked_workshifts': booked_workshifts})

@login_required
def work_shifts(request):
    user_profile = request.user.profile
    booked_workshifts = Booking.objects.filter(user=user_profile.user)
    return render(request, 'profiles/profile_detail.html', {'booked_workshifts': booked_workshifts})

def links(request):
    employees = Profile.objects.all()
    return render(request, 'profiles/links.html', {'employees': employees})

def knowledge_base(request):
    employees = Profile.objects.all()
    return render(request, 'profiles/knowledgebase.html', {'employees': employees})

@login_required
def employees(request):
    users = User.objects.order_by('first_name')

    # Pagination
    paginator = Paginator(users, 5)  # Show 5 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employees.html', {'page_obj': page_obj, 'users': page_obj.object_list})

@staff_member_required
def admin_view_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles/admin_view_profiles.html', {'profiles': profiles})
