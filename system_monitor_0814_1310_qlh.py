# 代码生成时间: 2025-08-14 13:10:57
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import PermissionDenied
import psutil
import platform
import datetime

"""
Views module for monitoring system performance.
This module provides views for gathering CPU, memory, and disk usage statistics.
"""

class SystemPerformanceMonitor(View):
    """
    A view to monitor system performance.
    It provides CPU, memory, and disk usage statistics.
    """
    def get(self, request, *args, **kwargs):
        # Check if the request is authorized
        if not request.user.is_authenticated:
            raise PermissionDenied('User is not authenticated')

        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            system_info = {
                'os': platform.platform(),
                'cpu_usage': cpu_usage,
                'memory_total': memory.total,
                'memory_available': memory.available,
                'memory_used': memory.used,
                'memory_usage_percentage': memory.percent,
                'disk_total': disk_usage.total,
                'disk_used': disk_usage.used,
                'disk_free': disk_usage.free,
                'disk_usage_percentage': disk_usage.percent,
            }
            return JsonResponse(system_info, safe=False)
        except Exception as e:
            # Handle any exceptions that may occur during system monitoring
            return JsonResponse({'error': str(e)}, status=500)


def get_urls():
    """
    Returns the URL patterns for the system performance monitor.
    """
    from django.urls import path
    from .views import SystemPerformanceMonitor

    urlpatterns = [
        path('system-monitor/', SystemPerformanceMonitor.as_view(), name='system-monitor'),
    ]
    return urlpatterns
