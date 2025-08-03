# 代码生成时间: 2025-08-03 21:27:37
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# Models
class Notification(models.Model):
    """Model to store notifications."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}: {self.message} at {self.timestamp}"

# Views
class NotificationView(View):
    """View to handle notification logic."""
    def get(self, request, *args, **kwargs):
        """Retrieves all notifications for the logged-in user."""
        try:
            notifications = Notification.objects.filter(user=request.user, seen=False)
            return JsonResponse(list(notifications.values()), safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    def post(self, request, *args, **kwargs):
        "