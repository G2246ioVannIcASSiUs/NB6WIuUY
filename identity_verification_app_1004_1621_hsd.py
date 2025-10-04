# 代码生成时间: 2025-10-04 16:21:41
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator

# Models
class User(models.Model):
    # 用户名
    username = models.CharField(max_length=150, unique=True)
    # 年龄
    age = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.username

# Views
@csrf_exempt
@require_http_methods(['POST'])
def verify_identity(request):
    """
    Verify if the provided identity information is valid.
    This view expects a POST request with JSON data containing 'username' and 'age'.
    If the username and age are valid, it will return a success response.
    """
    try:
        # Extract data from POST request
        data = request.POST
        username = data.get('username')
        age = int(data.get('age'))

        # Validate data
        if not username or not age:
            raise ValueError("Username and age are required.")

        # Check if user exists and age is positive
        user, created = User.objects.get_or_create(username=username)
        user.age = age
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Identity verified successfully.'}, status=200)
    except (User.DoesNotExist, ValueError, ValidationError) as e:
        # Handle exceptions and return error messages
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    except Exception as e:
        # General exception handling
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'}, status=500)

# URLs
from django.urls import path

urlpatterns = [
    path('verify/', verify_identity, name='verify_identity'),
]
