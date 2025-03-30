from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile

def signupuser(request):
    """
    Handle user registration.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the main page or render the signup form.
    :rtype: HttpResponse
    """
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})

def loginuser(request):
    """
    Handle user login.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the main page or render the login form.
    :rtype: HttpResponse
    """
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, _('Username or password didn\'tmatch'))
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quotes_app:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    """
    Handle user logout.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Redirect to the main page.
    :rtype: HttpResponse
    """
    logout(request)
    return redirect(to='quotes_app:main')

@login_required
def profile(request):
    """
    Display and update the user's profile.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Render the profile page or redirect after updating the profile.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=Profile.objects.get_or_create(user=request.user)[0])
    return render(request, 'users/profile.html', {'profile_form': profile_form})

class CustomPasswordResetView(PasswordResetView):
    """
    Custom view for handling password reset requests.
    """
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    subject_template_name = 'users/password_reset_subject.txt'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom view for handling password reset confirmation.
    """
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')