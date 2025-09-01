# 代码生成时间: 2025-09-02 05:28:39
# math_tool_app/math_tool_app/__init__.py
defmodule_init():
    pass

# math_tool_app/math_tool_app/apps.py
from django.apps import AppConfig


class MathToolAppConfig(AppConfig):
    name = 'math_tool_app'

# math_tool_app/math_tool_app/models.py
from django.db import models

class MathCalculation(models.Model):
    # 存储数学计算结果
    calculation = models.CharField(max_length=255)
    result = models.DecimalField(max_digits=20, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.calculation

# math_tool_app/math_tool_app/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import MathCalculation
from django.core.exceptions import ValidationError
import json


def math_toolbox_view(request):
    """
    A view that handles math calculation requests.
    
    Args:
        request (HttpRequest): The HTTP request from the client.
    
    Returns:
        JsonResponse: A JSON response with the calculation result.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            calculation = data.get('calculation')
            if not calculation:
                raise ValueError("Calculation parameter is missing.")
            result = evaluate_calculation(calculation)
            save_result(calculation, result)
            return JsonResponse({'result': result}, status=200)
        except (ValueError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed.'}, status=405)

# math_tool_app/math_tool_app/urls.py
from django.urls import path
from .views import math_toolbox_view

urlpatterns = [
    path('math-toolbox/', math_toolbox_view, name='math_toolbox_view'),
]

# math_tool_app/math_tool_app/utils.py
from math import *


def evaluate_calculation(calculation):
    """
    Evaluates a mathematical calculation string.
    
    Args:
        calculation (str): A string representing a mathematical calculation.
    
    Returns:
        float: The result of the calculation.
    
    Raises:
        ValueError: If the calculation is invalid.
    """
    try:
        return eval(calculation)
    except Exception as e:
        raise ValueError('Invalid calculation') from e


def save_result(calculation, result):
    """
    Saves the result of a calculation to the database.
    
    Args:
        calculation (str): The calculation performed.
        result (float): The result of the calculation.    
    """
    MathCalculation.objects.create(calculation=calculation, result=result)