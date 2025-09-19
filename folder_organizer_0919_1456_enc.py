# 代码生成时间: 2025-09-19 14:56:26
# folder_organizer\application\models.py"
"""
Models for the folder organizer application.
"""
from django.db import models"

class Folder(models.Model):
    """A model representing a folder."""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# folder_organizer\application\views.py"
"""
Views for the folder organizer application.
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Folder
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
import os
from django.conf import settings

@require_http_methods(['GET', 'POST'])
def organize_folders(request):
    """
    Organize files in the given directory.
    If a POST request is made, a folder name is expected in the data.
    For GET requests, return the current structure of the directories.
    """
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        folder_path = request.POST.get('folder_path')

        # Error handling for non-existent directory
        if not default_storage.exists(folder_path):
            return JsonResponse({'error': 'Directory does not exist'}, status=404)

        # Create a new folder
        try:
            new_folder = Folder.objects.create(name=folder_name, parent=None)
            new_folder_path = os.path.join(folder_path, folder_name)
            default_storage.save(new_folder_path, default_storage.open(new_folder_path, 'w'))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Folder created successfully'}, status=201)
    else:
        # Return the structure of folders
        try:
            folders = Folder.objects.all()
            folder_structure = []
            for folder in folders:
                folder_structure.append({'id': folder.id, 'name': folder.name, 'parent': folder.parent_id})

            return JsonResponse({'folders': folder_structure}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No folders found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# folder_organizer\application\urls.py"
"""
URLs for the folder organizer application.
"""
from django.urls import path"
from . import views

urlpatterns = [
    path('organize/', views.organize_folders, name='organize_folders'),
]

# folder_organizer\application	ests.py"
"""
Tests for the folder organizer application.
"""
from django.test import TestCase
from django.urls import reverse
from .models import Folder
from django.core.files.storage import default_storage
import os

class FolderOrganizerTestCase(TestCase):
    def setUp(self):
        self.folder = Folder.objects.create(name='Test Folder', parent=None)
        self.folder_path = os.path.join(settings.MEDIA_ROOT, self.folder.name)

    def test_folder_creation(self):
        response = self.client.post(reverse('organize_folders'), data={'folder_name': 'New Folder', 'folder_path': self.folder_path})
        self.assertEqual(response.status_code, 201)

    def test_folder_structure(self):
        response = self.client.get(reverse('organize_folders'))
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        default_storage.delete(self.folder_path)
        self.folder.delete()
