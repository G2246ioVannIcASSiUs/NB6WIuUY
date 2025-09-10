# 代码生成时间: 2025-09-10 17:18:09
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
# TODO: 优化性能
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
"""
Django application for user authentication.
This application includes models, views, and URLs for user authentication.
"""
# NOTE: 重要实现细节

# Define a custom error message for authentication errors.
AUTHENTICATION_ERROR_MSG = "Invalid credentials. Please try again."

class AuthView(View):
    """
    View for handling user authentication.
    Provides endpoints for login and logout.
    """
    def get(self, request):
        # If the user is already authenticated, redirect to a home page.
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'login.html')

    def post(self, request):
        # Attempt to authenticate the user.
# 添加错误处理
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # If authentication is successful, log the user in.
                login(request, user)
                return redirect('home')
            else:
# 改进用户体验
                # Return an error message if authentication fails.
                return JsonResponse({'error': AUTHENTICATION_ERROR_MSG})
        else:
            # Return an error message if username or password is not provided.
# 扩展功能模块
            return JsonResponse({'error': 'Username and password are required.'})

@login_required
def logout_view(request):
    """
    View for handling user logout.
    """
# 优化算法效率
    logout(request)
    return redirect('login')

# Define the URL patterns for the authentication views.
urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
