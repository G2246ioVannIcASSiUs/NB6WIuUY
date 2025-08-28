# 代码生成时间: 2025-08-29 05:10:32
# audit_log_app/__init__.py
# 初始化文件，确保Django识别该目录为应用

# audit_log_app/models.py
"""
Models for the Audit Log application in Django.
"""
from django.db import models
from django.contrib.auth.models import User
import uuid

class AuditLog(models.Model):
    """
    Represents an audit log entry.
    Each instance logs a user's action along with other relevant data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, help_text="The action performed by the user.")
    description = models.TextField(blank=True, help_text="A detailed description of the action.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """String representation of the Audit Log entry."""
        return f"{self.user.username} - {self.action} at {self.created_at}"

# audit_log_app/views.py
"""
Views for the Audit Log application in Django.
"""
from django.shortcuts import render
from .models import AuditLog

def audit_log_view(request):
    """
    Display the audit logs.
    This view fetches all audit log entries and passes them to a template for display.
    """
    logs = AuditLog.objects.all().order_by('-created_at')
    return render(request, 'audit_log_app/audit_logs.html', {'logs': logs})

# audit_log_app/urls.py
"""
URL configuration for the Audit Log application.
"""
from django.urls import path
from .views import audit_log_view

urlpatterns = [
    path('logs/', audit_log_view, name='audit-logs'),
]

# audit_log_app/admin.py
"""
Django admin interface customization for the Audit Log application."""
from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    Custom admin interface for AuditLog model.
    Provides a simple way to view and manage audit logs.
    """
    list_display = ('id', 'user', 'action', 'created_at')
    search_fields = ('user__username', 'action')
    list_filter = ('user', 'action')

# audit_log_app/tests.py
"""
Tests for the Audit Log application.
"""
from django.test import TestCase
from .models import AuditLog
from django.contrib.auth.models import User
import uuid

class AuditLogTestCase(TestCase):
    """
    Test cases for the Audit Log model and views.
    """
    def test_audit_log_creation(self):
        """
        Test that an audit log is created when a user action is logged.
        """
        user = User.objects.create_user(username='testuser', password='password')
        action = 'Test Action'
        AuditLog.objects.create(user=user, action=action)
        self.assertEqual(AuditLog.objects.count(), 1)

# audit_log_app/forms.py
"""
Forms for the Audit Log application.
"""
from django import forms
from .models import AuditLog

class AuditLogForm(forms.ModelForm):
    """
    A form for creating Audit Log entries.
    """
    class Meta:
        model = AuditLog
        fields = ['user', 'action', 'description']
        
    # You can add validation here if needed
