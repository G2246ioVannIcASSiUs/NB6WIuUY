# 代码生成时间: 2025-09-19 04:01:49
from django.apps import AppConfig
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
import json
import chartkick

# models.py
class ChartData(models.Model):
    """Model to store chart data."""
    data = models.TextField(help_text="JSON data for the chart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ChartData {self.id}'

# views.py
class ChartView(View):
    """View to handle chart data and rendering."""
    def get(self, request, *args, **kwargs):
        try:
            chart_data = ChartData.objects.all()
            return render(request, 'chart.html', {'chart_data': chart_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        "