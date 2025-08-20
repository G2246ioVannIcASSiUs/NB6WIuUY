# 代码生成时间: 2025-08-20 23:31:25
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist

# models.py
"""
Defines the models for the Notification app.
"""

class Message(models.Model):
    """
    Represents a message that can be sent to a user.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.user.username} at {self.created_at}"

# views.py
"""
Handles requests for the Notification app.
"""

class SendMessageView(View):
    """
    Handles sending a message to a user.
    """
    def post(self, request):
        """
        Receives a POST request to send a message to a user.
        """
        try:
            user_id = request.POST.get('user_id')
            content = request.POST.get('content')
            if not user_id or not content:
                return JsonResponse({'error': 'Missing user_id or content.'}, status=400)
            
            user = request.user  # Assuming the sender is the currently authenticated user
            message = Message.objects.create(user=user, content=content)
            return JsonResponse({'id': message.id, 'content': message.content}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# urls.py
"""
Defines the URL patterns for the Notification app.
"""

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
]

# To include the notification app in your Django project, add the following to your project's urls.py:

# from django.urls import include, path
# from notification_app import urls as notification_urls
# urlpatterns = [
#     ...
#     path('notifications/', include(notification_urls)),
# ]