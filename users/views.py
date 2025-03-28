from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile

def signupuser(request):
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
    logout(request)
    return redirect(to='quotes_app:main')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')

    profile_form = ProfileForm(instance=Profile.objects.get_or_create(user=request.user)[0])
    return render(request, 'users/profile.html', {'profile_form': profile_form})