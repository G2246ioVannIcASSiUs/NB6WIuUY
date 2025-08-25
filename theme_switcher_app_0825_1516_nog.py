# 代码生成时间: 2025-08-25 15:16:22
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# 定义一个用于管理主题切换的视图
@csrf_exempt
def switch_theme(request):
    """
    Endpoint to switch themes for the current user.
    
    Args:
        request (HttpRequest): The current request.
    
    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == 'POST':
        try:
            # 获取当前登录用户
            current_user = request.user
            # 从请求体中获取新的主题
            new_theme = request.POST.get('theme')
            # 检查新主题是否有效
            if new_theme and new_theme in settings.THEME_CHOICES:
                # 将新主题保存至用户的profile
                current_user.profile.theme = new_theme
                current_user.profile.save()
                return JsonResponse({'message': 'Theme switched successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid theme.'}, status=400)
        except Exception as e:
            # 记录错误信息
            messages.error(request, 'Error switching theme: {}'.format(str(e)))
            return JsonResponse({'error': 'Error switching theme.'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('switch_theme/', views.switch_theme, name='switch_theme'),
]

# models.py
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    """
    A model representing a user profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=100, default='light')

    def __str__(self):
        return self.user.username

# views.py
from django.shortcuts import render
from .models import UserProfile

# 其他视图可以按照Django最佳实践来实现

# 假设这里有一个视图函数来显示当前主题
def current_theme(request):
    """
    Displays the current theme of the user.
    
    Args:
        request (HttpRequest): The current request.
    
    Returns:
        HttpResponse: A response with the current theme.
    """
    user_theme = UserProfile.objects.get(user=request.user).theme
    return HttpResponse(f'Current theme is: {user_theme}')
