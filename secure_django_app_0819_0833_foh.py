# 代码生成时间: 2025-08-19 08:33:16
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
import logging

# Create your models here.
class User(models.Model):
    """ Model for user details. """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

# Create your views here.
class UserListView(View):
    """
    View to list all users. Prevents SQL Injection by using Django's ORM which is
    designed to be safe from such attacks.
    """
    def get(self, request):
        # Use Django's ORM to query the database safely.
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})

    def post(self, request):
        # Example of preventing SQL injection through proper form validation and ORM usage.
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            User.objects.create(username=username, email=email)
            return HttpResponse("User created successfully.")
        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            return HttpResponse("Invalid input.", status=400)

# Create your urls here.
from django.urls import path
from .views import UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
]

# templates/users.html - example template for listing users.
# {% for user in users %}
# <li>{{ user.username }} - {{ user.email }}</li>
# {% endfor %}

# logging configuration can be added in settings.py under LOGGING.