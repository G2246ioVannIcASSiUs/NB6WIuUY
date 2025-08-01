# 代码生成时间: 2025-08-01 15:01:20
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from PIL import Image
import os

"""
Image Resizer App

This Django app provides functionality to resize multiple images at once.
"""


class ImageModel(models.Model):
    """Model to store image file paths."""
    file_path = models.CharField(max_length=255)
    original_size = models.TupleField(max_length=2)

    def __str__(self):
        return self.file_path

    class Meta:
        verbose_name_plural = "Images"


class ResizeImageView(View):
    """
    View to handle image resizing.

    Accepts a POST request with JSON data containing a list of image paths and a tuple for the new size.
    Returns a JSON response with the resized image paths.
    """
    def post(self, request, *args, **kwargs):
        # Get the list of images and the new size from the request body
        data = request.POST.get('data', '{}')
        try:
            image_data = json.loads(data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        image_paths = image_data.get('images', [])
        new_size = image_data.get('size', (0, 0))
        resized_images = []

        # Check if the new size is valid
        if not all(isinstance(dim, int) and dim > 0 for dim in new_size):
            return JsonResponse({'error': 'Invalid new size'}, status=400)

        # Resize the images
        for image_path in image_paths:
            try:
                with Image.open(image_path) as img:
                    img.thumbnail(new_size)
                    # Save the resized image with a suffix
                    resized_path = image_path + '_resized'
                    img.save(resized_path)
                    resized_images.append(resized_path)
            except IOError:
                return JsonResponse({'error': f'Could not open or process image: {image_path}'}, status=500)

        # Return the list of resized image paths
        return JsonResponse({'resized_images': resized_images})


def image_resizer_urls():
    """
    Returns the URL patterns for the image resizer app.
    """
    return [
        path('resize/', ResizeImageView.as_view(), name='resize_image'),
    ]


# Assuming you have the following settings in your Django project settings.py
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
