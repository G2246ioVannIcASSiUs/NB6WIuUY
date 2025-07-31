# 代码生成时间: 2025-07-31 13:22:26
# notification_app/models.py
"""
This module contains the models for the notification system.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Notification(models.Model):
    """
    A model to represent a notification.
    """
    message = models.TextField(help_text="The message of the notification.")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification to {self.recipient}: {self.message[:30]}..."


# notification_app/views.py
"""
This module contains the views for the notification system.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Notification
from django.db import transaction

@csrf_exempt
@require_http_methods(['POST'])
def notify_view(request):
    """
    A view to create a new notification.
    
    Args:
        request (HttpRequest): The HTTP request object.
    """
    try:
        with transaction.atomic():
            data = request.POST
            recipient_id = data['recipient_id']
            message = data['message']
            recipient = User.objects.get(pk=recipient_id)
            notification = Notification.objects.create(
                message=message,
                recipient=recipient
            )
            return JsonResponse({'id': notification.id, 'message': 'Notification sent successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def mark_notifications_as_read(request, user_id):
    """
    A view to mark notifications as read for a given user.
    
    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The ID of the user whose notifications are to be marked as read.
    """
    try:
        user_notifications = Notification.objects.filter(recipient_id=user_id, is_read=False)
        user_notifications.update(is_read=True)
        return JsonResponse({'message': 'Notifications marked as read successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# notification_app/urls.py
"""
This module contains the URL patterns for the notification system.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('notify/', views.notify_view, name='notify'),
    path('mark-read/<int:user_id>/', views.mark_notifications_as_read, name='mark_read'),
]

# notification_app/apps.py
"""
This module defines the configuration for the notification app.
"""
from django.apps import AppConfig

class NotificationConfig(AppConfig):
    name = 'notification_app'
    verbose_name = 'Notification'

    def ready(self):
        # Import signal handlers, checks, and other startup configurations.
        pass