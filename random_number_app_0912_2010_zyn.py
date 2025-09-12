# 代码生成时间: 2025-09-12 20:10:44
//random_number_app/models.py
"""
随机数生成器的数据库模型
"""
from django.db import models
def generate_random_number():
    """
    生成一个随机数

    Returns:
        int: 随机生成的整数
    """
    import random
    return random.randint(0, 100)

def generate_random_number_in_range(min, max):
    """
    生成指定范围内的随机数

    Args:
        min (int): 范围的最小值
        max (int): 范围的最大值

    Returns:
        int: 随机生成的整数
    """
    import random
    return random.randint(min, max)


//random_number_app/views.py
"""
随机数生成器的视图
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
def generate_random_number_view(request):
    """
    生成并返回一个随机数

    Args:
        request (HttpRequest): 客户端请求

    Returns:
        JsonResponse: 包含随机数的JSON响应
    """
    return JsonResponse({'random_number': generate_random_number()})
def generate_random_number_in_range_view(request, min, max):
    """
    生成并返回指定范围内的随机数

    Args:
        request (HttpRequest): 客户端请求
        min (int): 范围的最小值
        max (int): 范围的最大值

    Returns:
        JsonResponse: 包含随机数的JSON响应
    """
    try:
        random_number = generate_random_number_in_range(int(min), int(max))
        return JsonResponse({'random_number': random_number})
    except ValueError:
        return JsonResponse({'error': 'Invalid input values'}, status=400)

@require_http_methods(['GET'])
def generate_random_number_in_range_endpoint(request):
    """
    处理生成指定范围内随机数的请求

    Args:
        request (HttpRequest): 客户端请求

    Returns:
        JsonResponse: 包含随机数的JSON响应
    """
    min = request.GET.get('min')
    max = request.GET.get('max')
    if not min or not max:
        return JsonResponse({'error': 'Missing input values'}, status=400)
    if min.isdigit() and max.isdigit() and int(min) < int(max):
        return generate_random_number_in_range_view(request, int(min), int(max))
    else:
        return JsonResponse({'error': 'Invalid input values'}, status=400)

//random_number_app/urls.py
"""
定义随机数生成器的URL路由
"""
from django.urls import path
from .views import generate_random_number_view, generate_random_number_in_range_endpoint
app_name = 'random_number_app'
urlpatterns = [
    path('random_number/', generate_random_number_view, name='generate_random_number'),
    path('random_number_in_range/', generate_random_number_in_range_endpoint, name='generate_random_number_in_range'),
]

//random_number_app/apps.py
"""
随机数生成器应用的配置
"""
from django.apps import AppConfig
def ready(self):
    """
    应用启动时执行的操作
    """
    pass

class RandomNumberAppConfig(AppConfig):
    """
    随机数生成器应用的配置类
    """
    name = 'random_number_app'