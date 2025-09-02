# 代码生成时间: 2025-09-02 13:07:14
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import path
from django.views import View
from django.utils import timezone
import logging

# 配置日志
logger = logging.getLogger(__name__)

class Notification(models.Model):
    """消息通知模型"""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

@require_http_methods(['POST'])
def send_notification(request):
    """发送通知"""
    try:
        user_id = request.POST.get('user_id')
        title = request.POST.get('title')
        message = request.POST.get('message')
        
        if not all([user_id, title, message]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        user = User.objects.get(id=user_id)
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message
        )
        return JsonResponse({'message': 'Notification sent successfully', 'id': notification.id}, status=201)
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except Exception as e:
        logger.error(f'Error sending notification: {str(e)}')
        return JsonResponse({'error': 'Internal server error'}, status=500)

@require_http_methods(['GET'])
def get_notifications(request):
    """获取用户通知"""
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        
        user = User.objects.get(id=user_id)
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        return JsonResponse({'notifications': [
            {'id': n.id, 'title': n.title, 'message': n.message, 'is_read': n.is_read, 'created_at': n.created_at.isoformat()}
            for n in notifications
        ]}, status=200)
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist")
        return JsonResponse({'error': 'User does not exist'}, status=404)
    except Exception as e:
        logger.error(f'Error retrieving notifications: {str(e)}')
        return JsonResponse({'error': 'Internal server error'}, status=500)

# URL配置
urlpatterns = [
    path('send/', send_notification, name='send_notification'),
    path('get/', get_notifications, name='get_notifications'),
]
