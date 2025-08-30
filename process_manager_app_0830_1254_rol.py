# 代码生成时间: 2025-08-30 12:54:48
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import subprocess
import shlex
import os
import signal
import psutil

"""
A Django application component to manage system processes.

This component includes models for storing process information, views for handling process management
requests, and URL configurations for routing these requests.
"""

# Models
class Process(models.Model):
    """
    A model to store information about system processes.
    """
    process_name = models.CharField(max_length=255, unique=True)
    process_id = models.IntegerField(unique=True)
    process_status = models.BooleanField(default=False)

    def __str__(self):
        return self.process_name

# Views
class ProcessManagerView(View):
    """
    A view for managing system processes.
    """
    def get(self, request):
        """
        Retrieve a list of all processes.
        """
        processes = Process.objects.all()
        data = []
        for process in processes:
            data.append({
                'process_name': process.process_name,
                'process_id': process.process_id,
                'process_status': process.process_status
            })
        return JsonResponse(data, safe=False)

    @require_http_methods(['POST'])
    def post(self, request):
        """
        Start a new process.
        """
        try:
            command = request.POST.get('command')
            if not command:
                return JsonResponse({'error': 'Command not provided'}, status=400)

            # Execute the command
            process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Store the process information in the database
            new_process = Process.objects.create(
                process_name=command,
                process_id=process.pid,
                process_status=True
            )
            return JsonResponse({'message': 'Process started successfully', 'process_id': process.pid})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @require_http_methods(['PUT'])
    def put(self, request, process_id):
        """
        Update the status of a process.
        """
        try:
            process = Process.objects.get(process_id=process_id)
            process.process_status = not process.process_status
            process.save()
            return JsonResponse({'message': 'Process status updated successfully'})
        except Process.DoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @require_http_methods(['DELETE'])
    def delete(self, request, process_id):
        """
        Terminate a process.
        """
        try:
            process = Process.objects.get(process_id=process_id)
            if psutil.pid_exists(process.process_id):
                os.kill(process.process_id, signal.SIGTERM)
                process.process_status = False
                process.save()
            return JsonResponse({'message': 'Process terminated successfully'})
        except Process.DoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# URL Configuration
urlpatterns = [
    path('processes/', ProcessManagerView.as_view(), name='processes'),
]
