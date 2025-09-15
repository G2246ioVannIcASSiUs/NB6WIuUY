# 代码生成时间: 2025-09-16 07:50:06
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path
from django.views import View
import os
from django.utils import timezone
import re

def validate_new_filename(value):
    """Validate that the filename is not empty and does not contain invalid characters."""
    if not value:
        raise ValidationError('Filename cannot be empty.')
    if re.match(r'[^a-zA-Z0-9_ -]', value):
        raise ValidationError('Filename contains invalid characters.')

class BulkRename(models.Model):
    """Model to store file rename operations."""
    original_name = models.CharField(max_length=255)
    new_name = models.CharField(max_length=255, blank=True, null=True, validators=[validate_new_filename])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    """Auto-set fields for creation and update timestamps."""

    def __str__(self):
        return self.original_name

class BulkRenameView(View):
    """View to handle the bulk rename operation."""
    def get(self, request, *args, **kwargs):
        """GET request to display the bulk rename form."""
        return render(request, 'bulk_rename_form.html')

    def post(self, request, *args, **kwargs):
        """POST request to handle bulk rename operation."""
        files_to_rename = request.POST.getlist('files[]')
        new_names = request.POST.getlist('new_names[]')
        rename_errors = []
        for original, new in zip(files_to_rename, new_names):
            try:
                BulkRename.objects.create(original_name=original, new_name=new)
                os.rename(os.path.join(settings.MEDIA_ROOT, original), os.path.join(settings.MEDIA_ROOT, new))
            except Exception as e:
                rename_errors.append(f"Error renaming {original} to {new}: {str(e)}")
        if rename_errors:
            return JsonResponse({'errors': rename_errors}, status=400)
        return JsonResponse({'message': 'Files renamed successfully.'})

# urls.py
urlpatterns = [
    path('bulk_rename/', BulkRenameView.as_view(), name='bulk_rename'),
]
