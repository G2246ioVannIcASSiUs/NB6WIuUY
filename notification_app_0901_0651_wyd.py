# 代码生成时间: 2025-09-01 06:51:38
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.utils import timezone

"""
A Django application component for a message notification system.
"""

class Notification(models.Model):
    """
    A model representing a notification.
    
    Attributes:
        title (str): The title of the notification.
        message (str): The message content of the notification.
        created_at (datetime): The time when the notification was created.
        sent_at (datetime): The time when the notification was sent.
        email_sent (bool): Whether the notification email has been sent.
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.created_at}"

    def send_notification(self):
        """
        Send the notification via email.
        
        If the email is successfully sent, update the sent_at field and set email_sent to True.
        """
        try:
            send_mail(
                self.title,
                self.message,
                settings.EMAIL_HOST_USER,
                [settings.NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            self.sent_at = timezone.now()
            self.email_sent = True
            self.save()
        except Exception as e:
            # Log the exception or handle the error as required
            print(f"Error sending notification: {e}")

@csrf_exempt
@require_http_methods(['POST'])
def create_notification(request: HttpRequest) -> JsonResponse:
    """
    Create a new notification and send it via email.
    
    Args:
        request (HttpRequest): The HTTP request containing the notification data.
        
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the operation.
    """
    try:
        data = request.POST
        title = data.get('title')
        message = data.get('message')
        if not title or not message:
            return JsonResponse({'error': 'Title and message are required'}, status=400)
        notification = Notification.objects.create(title=title, message=message)
        notification.send_notification()
        return JsonResponse({'message': 'Notification created and sent successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

urlpatterns = [
    path('create_notification/', create_notification, name='create_notification'),
]
