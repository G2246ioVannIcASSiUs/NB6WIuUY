# 代码生成时间: 2025-10-09 03:57:22
# interactive_chart_generator_app/__init__.py
# This file can be left empty.

# interactive_chart_generator_app/models.py
"""
This module contains the models representing chart data.
"""
from django.db import models
def create_chart_data_model():
    class ChartData(models.Model):
        """
        A model for storing chart data.
        
        Attributes:
            title (str): The title of the chart.
            data (JSONField): The data to be displayed on the chart.
        """
        title = models.CharField(max_length=255)
        data = models.JSONField()

    return ChartData

# interactive_chart_generator_app/views.py
"""
This module contains the views for the interactive chart generator app.
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import create_chart_data_model
import json

ChartData = create_chart_data_model()

@require_http_methods(["GET", "POST"])
def chart_data_view(request):
    """
    View to handle chart data requests.
    
    On GET request, it returns a list of all chart data.
    On POST request, it creates a new chart data entry.
    
    Args:
        request (HttpRequest): The Django HTTP request.
    
    Returns:
        JsonResponse: A JSON response with the chart data or error message.
    """
    if request.method == "GET":
        chart_data_list = ChartData.objects.all()
        return JsonResponse(list(chart_data_list.values()), safe=False)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            chart_data = ChartData.objects.create(
                title=data.get("title"),
                data=data.get("data")
            )
            return JsonResponse(chart_data.__dict__, safe=False)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
        except Exception as e:
            return HttpResponse(str(e), status=500)

# interactive_chart_generator_app/urls.py
"""
This module contains the URL patterns for the interactive chart generator app.
"""
from django.urls import path
from .views import chart_data_view

urlpatterns = [
    path("chart-data/", chart_data_view, name="chart-data"),
]
