# 代码生成时间: 2025-09-14 07:12:11
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


"""
A Django app component for user authentication.
This module provides views for user registration and login,
as well as protected views that require authentication.
"""


# Define models
class User(models.Model):
    pass  # Use Django's built-in User model


# Define forms
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# Define views
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    """
    Handle user login.
    Returns a JSON response with login status.
    """
    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Logged in successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid username or password.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(View):
    """
    Handle user registration.
    Returns a JSON response with registration status.
    """
    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return JsonResponse({'status': 'success', 'message': 'Registered successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@login_required
class UserProfileView(View):
    """
    Handle user profile page.
    Requires authentication.
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html')


# Define URLs
from django.urls import path

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]