# 代码生成时间: 2025-08-17 13:34:01
from django.apps import AppConfig
def ready():
    # 这个函数在Django启动时会被调用，用于应用级别的初始化
    pass

# 以下是使用Django最佳实践创建的日志文件解析工具的代码

# models.py
from django.db import models

"""
Model for storing log files and their parsed data.
"""
class LogFile(models.Model):
    """
    Represents a log file.
    """
    file_path = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_path

class LogEntry(models.Model):
    """
    Represents a single entry within a log file.
    """
    log_file = models.ForeignKey(LogFile, on_delete=models.CASCADE, related_name='entries')
    timestamp = models.DateTimeField()
    level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.level} - {self.message[:50]}..."

# views.py
from django.http import JsonResponse
from .models import LogFile, LogEntry
import logging
import os
from datetime import datetime

"""
Views for handling log file operations.
"""

logger = logging.getLogger(__name__)

def parse_log_file(request, file_path):
    """
    Parses a log file and returns the parsed log entries.
    
    Args:
    - request: HttpRequest object.
    - file_path: Path to the log file.
    
    Returns:
    - JsonResponse with the parsed log entries.
    """
    try:
        log_file, created = LogFile.objects.get_or_create(file_path=file_path)
        log_entries = []
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming the log format is 'timestamp level message'
                parts = line.strip().split(' ', 2)
                if len(parts) == 3:
                    timestamp, level, message = parts
                    log_entry, created = LogEntry.objects.update_or_create(
                        log_file=log_file,
                        timestamp=timestamp,
                        defaults={'level': level, 'message': message}
                    )
                    log_entries.append({'timestamp': timestamp, 'level': level, 'message': message})
        return JsonResponse({'log_entries': log_entries}, safe=False)
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return JsonResponse({'error': 'File not found.'}, status=404)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return JsonResponse({'error': 'An error occurred while parsing the log file.'}, status=500)

# urls.py
from django.urls import path
from . import views

"""
URL patterns for the log parser app.
"""
urlpatterns = [
    path('parse/<path:file_path>/', views.parse_log_file, name='parse_log_file'),
]
