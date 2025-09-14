# 代码生成时间: 2025-09-15 07:32:21
from django.db import models
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
from django.urls import path
from django.conf import settings
import zipfile
import os
import shutil
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist

# Define the model for storing compressed file information
def CompressedFile(models.Model):
    file = models.FileField(upload_to='compressed_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.file.name} uploaded at {self.created_at}"

    class Meta:
        verbose_name = 'Compressed File'
        verbose_name_plural = 'Compressed Files'


class UnzipToolView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """Endpoint to handle the upload and extraction of compressed files.
        
        Args:
            request (HttpRequest): The HTTP request containing the compressed file.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            JsonResponse: The response containing the status of the extraction process."""
        try:
            compressed_file = request.FILES['compressed_file']
            file_path = default_storage.save(compressed_file.name, ContentFile(compressed_file.read()))
            
            # Determine the extraction directory
            extraction_directory = os.path.join(settings.MEDIA_ROOT, 'extracted_files')
            if not os.path.exists(extraction_directory):
                os.makedirs(extraction_directory)
            
            # Extract the compressed file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extraction_directory)
            
            # Remove the uploaded compressed file
            os.remove(file_path)
            
            return JsonResponse({'status': 'success', 'message': 'File extracted successfully'})
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'No compressed file provided'})
        except zipfile.BadZipFile:
            return JsonResponse({'status': 'error', 'message': 'The file is not a valid zip file'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


def unzip_tool_urls():
    from django.urls import path
    return [
        path('unzip/', UnzipToolView.as_view(), name='unzip_tool'),
    ]

# Note: This code does not handle the creation of the CompressedFile model instance.
# In a real-world scenario, you would likely want to save a record of each uploaded file
# and potentially use that record to track the file's progress or status.
# This would involve modifying the UnzipToolView to handle file saving and
# potentially using signals or overriding the save method of the CompressedFile model.
