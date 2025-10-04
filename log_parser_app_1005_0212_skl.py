# 代码生成时间: 2025-10-05 02:12:22
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import re
import logging

# Define a model for storing log entries if needed
class LogEntry(models.Model):
    log_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.log_message

# Create your views here.
class LogParserView(View):
    def post(self, request, *args, **kwargs):
        # Get the log file content from the request
        log_content = request.POST.get('log_content')
        
        # Error handling for missing log content
        if not log_content:
            return JsonResponse({'error': 'Log content is required.'}, status=400)
        
        # Define a regular expression pattern for log entries
        log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(\w+)\s+(.*)")
        
        # Parse the log entries using the regex pattern
        entries = log_pattern.findall(log_content)
        
        # Store parsed log entries in a list
        parsed_entries = []
        for entry in entries:
            timestamp, level, message = entry
            parsed_entries.append({'timestamp': timestamp, 'level': level, 'message': message})
            
        # Optionally, save log entries to the database
        for entry in parsed_entries:
            LogEntry.objects.create(log_message=f"{entry['timestamp']} {entry['level']} {entry['message']}")
            
        # Return a JSON response with the parsed log entries
        return JsonResponse({'parsed_entries': parsed_entries}, safe=False)

# Define the URL pattern for the log parser view
urlpatterns = [
    path('parse_log/', LogParserView.as_view(), name='parse_log'),
]

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
