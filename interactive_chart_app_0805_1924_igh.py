# 代码生成时间: 2025-08-05 19:24:45
# interactive_chart_app/__init__.py

# interactive_chart_app/apps.py
from django.apps import AppConfig


class InteractiveChartAppConfig(AppConfig):
    name = 'interactive_chart_app'


# interactive_chart_app/models.py
from django.db import models

"""
Model for storing chart data.
"""
class ChartData(models.Model):
    # Example fields, adjust according to the chart data you need to store
    title = models.CharField(max_length=200)
    data = models.JSONField()  # Assumed to store data in JSON format

    def __str__(self):
        return self.title



# interactive_chart_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import ChartData
from django.views.decorators.http import require_http_methods

"""
View functions for the interactive chart application.
"""

@require_http_methods(['GET', 'POST'])
def chart_data_view(request):
    """
    Handle request to fetch or submit chart data.
    """
    if request.method == 'GET':
        try:
            # Fetch all chart data
            data_list = ChartData.objects.all()
            data = list(data_list.values('title', 'data'))
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            # Create new chart data
            title = request.POST.get('title')
            data = request.POST.get('data')
            chart_data = ChartData(title=title, data=data)
            chart_data.save()
            return JsonResponse({'message': 'Chart data saved successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# interactive_chart_app/urls.py
from django.urls import path
from .views import chart_data_view

"""
URL patterns for the interactive chart application.
"""
urlpatterns = [
    path('chart-data/', chart_data_view, name='chart-data'),
]


# interactive_chart_app/admin.py
from django.contrib import admin
from .models import ChartData

"""
Admin interface configurations for the interactive chart application.
"""
@admin.register(ChartData)
class ChartDataAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Customize admin list display


# interactive_chart_app/tests.py
from django.test import TestCase
from .models import ChartData

"""
Tests for the interactive chart application.
"""
class ChartDataTestCase(TestCase):
    def test_chart_data_creation(self):
        # Test creating a new chart data instance
        ChartData.objects.create(title='Test Chart', data='{"x": 1, "y": 2}')
        self.assertEqual(ChartData.objects.count(), 1)

    def test_chart_data_retrieval(self):
        # Test retrieving chart data
        chart_data = ChartData.objects.create(title='Test Chart', data='{"x": 1, "y": 2}')
        self.assertEqual(chart_data.title, 'Test Chart')

    def test_chart_data_update(self):
        # Test updating chart data
        chart_data = ChartData.objects.create(title='Test Chart', data='{"x": 1, "y": 2}')
        chart_data.title = 'Updated Chart'
        chart_data.save()
        self.assertEqual(chart_data.title, 'Updated Chart')

    def test_chart_data_deletion(self):
        # Test deleting chart data
        chart_data = ChartData.objects.create(title='Test Chart', data='{"x": 1, "y": 2}')
        chart_data.delete()
        self.assertEqual(ChartData.objects.count(), 0)


# settings.py (Add the following to your Django project settings)
INSTALLED_APPS = [
    ...
    'interactive_chart_app',
]

# Add URL pattern to your project's urls.py
from django.urls import include, path
urlpatterns = [
    ...
    path('charts/', include('interactive_chart_app.urls')),
]