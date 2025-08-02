# 代码生成时间: 2025-08-02 13:14:57
# permission_management_app/__init__.py
# Define your app's initialization code here

# permission_management_app/admin.py
from django.contrib import admin
from .models import UserPermission

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'permission')

# permission_management_app/apps.py
from django.apps import AppConfig

class PermissionManagementAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'permission_management_app'

# permission_management_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    """
    Model representing a permission that can be assigned to a user.
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Permission Name')

    def __str__(self):
        return self.name

class UserPermission(models.Model):
    """
    Model representing the assignment of a permission to a specific user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='assigned_to')

    class Meta:
        unique_together = ('user', 'permission')
        verbose_name = 'User Permission'
        verbose_name_plural = 'User Permissions'

    def __str__(self):
        return f"{self.user.username} - {self.permission.name}"

# permission_management_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Permission, UserPermission

class PermissionListView(View):
    """
    View to list all permissions.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        permissions = Permission.objects.all()
        return render(request, 'permissions/permission_list.html', {'permissions': permissions})

# permission_management_app/urls.py
from django.urls import path
from .views import PermissionListView

urlpatterns = [
    path('permissions/', PermissionListView.as_view(), name='permission-list'),
]

# permission_management_app/tests.py
from django.test import TestCase
from .models import Permission, UserPermission
from django.contrib.auth.models import User

class PermissionTestCase(TestCase):
    def setUp(self):
        self.permission = Permission.objects.create(name='edit_article')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_permission = UserPermission.objects.create(user=self.user, permission=self.permission)

    def test_permission_list(self):
        response = self.client.get('/permissions/')
        self.assertEqual(response.status_code, 200)

    def test_user_permission_assignment(self):
        self.assertEqual(self.user.permissions.count(), 1)
        self.assertEqual(self.user_permission.permission, self.permission)

# permission_management_app/forms.py
from django import forms
from .models import Permission

class PermissionForm(forms.ModelForm):
    """
    Form for creating and editing permissions.
    """
    class Meta:
        model = Permission
        fields = ('name',)

# permission_management_app/serializers.py
from rest_framework import serializers
from .models import Permission, UserPermission

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model.
    """
    class Meta:
        model = Permission
        fields = ('id', 'name',)

class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPermission model.
    """
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = UserPermission
        fields = ('id', 'user', 'permission',)
