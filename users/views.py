from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import RegisterForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin

def signupuser(request):
    """
    Handle user registration.
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
    """
    logout(request)
    return redirect(to='quotes_app:main')

@login_required
def profile(request):
    """
    Display and update the user's profile.
    """
    return render(request, 'users/profile.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom view for handling password reset confirmation.
    """
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')