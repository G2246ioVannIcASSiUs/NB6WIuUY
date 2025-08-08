# 代码生成时间: 2025-08-08 08:43:58
import os
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class FileBackup(models.Model):
    """Model to store file backup details."""
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

class FileBackupView(View):
    """View to handle file backup and synchronization operations."""
    def post(self, request, *args, **kwargs):
        """Backup a file and store its details."""
        try:
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'error': 'No file provided'}, status=400)

            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            file_size = file.size
            file_name = file.name
            with default_storage.open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            FileBackup.objects.create(file_name=file_name, file_size=file_size)
            return JsonResponse({'message': 'File backed up successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        """Synchronize the file system with the database records."""
        try:
            files = FileBackup.objects.all()
            for file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, file.file_name)
                if not default_storage.exists(file_path):
                    # Recreate missing files if necessary
                    default_storage.save(file_path, ContentFile(''))
            return JsonResponse({'message': 'Synchronization complete'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Define the URL patterns for the file backup tool
urlpatterns = [
    path('backup/', FileBackupView.as_view(), name='file_backup'),
]
