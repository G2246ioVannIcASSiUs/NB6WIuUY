# 代码生成时间: 2025-08-17 03:53:32
from django.db import models
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.urls import path
import datetime
import json

# Define the model for storing test results
class TestResult(models.Model):
    """Model to store test results."""
    test_name = models.CharField(max_length=255)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.test_name} - {self.start_time}"

# Create your views here.
class TestReportView(View):
    """View to generate test reports."""
    def get(self, request):
        try:
            test_results = TestResult.objects.all()
            report_data = []
            for result in test_results:
                report_data.append({
                    'test_name': result.test_name,
                    'start_time': result.start_time.isoformat(),
                    'end_time': result.end_time.isoformat(),
                    'status': result.status,
                    'comments': result.comments
                })
            # Generate the report in a JSON format
            report_json = json.dumps(report_data, indent=4)
            return HttpResponse(report_json, content_type='application/json')
        except Exception as e:
            return JsonResponse({'error': str(e)})

# Define the URL patterns for the view
urlpatterns = [
    path('generate-report/', TestReportView.as_view()),
]
