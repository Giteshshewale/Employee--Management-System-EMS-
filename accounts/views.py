import secrets

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, StyledPasswordChangeForm, ForgotPasswordForm
from .models import CustomUser


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            send_mail(
                subject='Welcome to Employee Management System',
                message=f'Hi {user.username}, your account has been created successfully.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email] if user.email else [],
                fail_silently=True,
            )
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard:dashboard')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = StyledPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = StyledPasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def forgot_password_view(request):
    """
    Optional simple 'forgot password' flow: verifies username+email match,
    generates a temporary random password, and emails it to the user
    (prints to console with the default dev email backend).
    """
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(username=username, email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, 'No matching account found.')
                return render(request, 'registration/forgot_password.html', {'form': form})

            temp_password = secrets.token_urlsafe(8)
            user.set_password(temp_password)
            user.save()
            send_mail(
                subject='Your temporary password',
                message=f'Your temporary password is: {temp_password}\nPlease log in and change it immediately.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
            messages.success(request, 'A temporary password has been sent to your email.')
            return redirect('accounts:login')
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})
