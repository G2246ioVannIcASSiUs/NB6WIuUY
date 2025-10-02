# 代码生成时间: 2025-10-02 18:28:05
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

"""
File Utility App

This Django app provides functionality to split and merge files.
"""

class FileSplitter(View):
    """
    A view to split a file into smaller parts.
    """
    def post(self, request):
        # Get file from request
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        # Split the file into chunks
        chunk_size = int(request.POST.get('chunk_size', 1024 * 1024))  # Default chunk size 1MB
        chunks = []
        with open(file.temporary_file_path(), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                chunks.append(ContentFile(chunk))
        
        # Save the chunks
        chunk_paths = []
        for i, chunk in enumerate(chunks):
            chunk_name = f"{file.name.split('.')[0]}_{i}.{file.name.split('.')[-1]}"
            default_storage.save(chunk_name, chunk)
            chunk_paths.append(chunk_name)
        
        return JsonResponse({'chunk_paths': chunk_paths})


class FileMerger(View):
    """
    A view to merge multiple files into one.
    """
    def post(self, request):
        # Get file names from request
        file_names = request.POST.getlist('file_names[]')
        if not file_names:
            return JsonResponse({'error': 'No file names provided'}, status=400)
        
        # Merge the files
        merged_file_name = request.POST.get('merged_file_name')
        if not merged_file_name:
            merged_file_name = 'merged_file'
        
        with default_storage.open(merged_file_name, 'wb') as merged_file:
            for file_name in file_names:
                with default_storage.open(file_name, 'rb') as f:
                    merged_file.write(f.read())
        
        return JsonResponse({'merged_file_name': merged_file_name})


# urls.py
from django.urls import path
from .views import FileSplitter, FileMerger

urlpatterns = [
    path('split/', FileSplitter.as_view(), name='file_splitter'),
    path('merge/', FileMerger.as_view(), name='file_merger'),
]
