# 代码生成时间: 2025-08-24 02:41:25
from django.apps import AppConfig


class InteractiveChartGeneratorConfig(AppConfig):
    """
    Django application configuration for the interactive chart generator.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interactive_chart_generator'


# models.py
from django.db import models
import json

# Define a model for storing chart data
class Chart(models.Model):
    """
    A model representing an interactive chart.
    """
    title = models.CharField(max_length=200)  # Chart title
    data = models.JSONField()  # JSON data for the chart
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for chart creation

    def __str__(self):
        """
        Returns a string representation of the Chart instance.
        """
        return self.title



# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Chart
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(['GET', 'POST'])
def chart_view(request):
    """
    View to handle chart data retrieval and submission.
    """
    if request.method == 'GET':
        # Return a list of all charts
        charts = Chart.objects.all()
        return JsonResponse(list(charts.values()), safe=False)
    elif request.method == 'POST':
        # Create a new chart from the provided data
        data = json.loads(request.body)
        chart = Chart(title=data['title'], data=data['data'])
        chart.save()
        return JsonResponse({'id': chart.id, 'title': chart.title}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# urls.py
from django.urls import path
from .views import chart_view

# Define the URL patterns for the interactive chart generator
urlpatterns = [
    path('charts/', chart_view, name='chart-list'),
]
