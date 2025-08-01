# 代码生成时间: 2025-08-01 23:10:50
import psutil
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import os

"""
Memory Analysis Application: Provides an interface to analyze the memory usage of the system.

This Django application includes a model to store memory usage data, views to handle HTTP requests,
and URLs to map to these views.
"""

class MemoryUsage(models.Model):
    """Model to store memory usage data."""
    timestamp = models.DateTimeField(auto_now_add=True)
    used_memory = models.BigIntegerField()
    available_memory = models.BigIntegerField()
    percentage_used = models.FloatField()

    def __str__(self):
        return f"MemoryUsage at {self.timestamp}: {self.percentage_used}% used"

# Views
@csrf_exempt
@require_http_methods(['GET'])
def memory_usage(request):
    "