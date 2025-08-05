# 代码生成时间: 2025-08-06 06:01:36
import zipfile
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os

"""
A Django view for unzipping uploaded zip files.
"""

class UnzipToolView(View):
    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Unzip the uploaded zip file.
        
        :param request: HttpRequest object containing the zip file.
        :return: JsonResponse indicating the success or failure of the operation.
        """
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided.'}, status=400)
        
        if not file.name.endswith('.zip'):
            return JsonResponse({'error': 'Invalid file type.'}, status=400)
        
        try:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(path=settings.MEDIA_ROOT)
            return JsonResponse({'message': 'File successfully unzipped.'}, status=200)
        except zipfile.BadZipFile:
            return JsonResponse({'error': 'Invalid zip file.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

"""
Define the URL patterns for the UnzipToolView.
"""
from django.urls import path

urlpatterns = [
    path('unzip/', UnzipToolView.as_view(), name='unzip_tool'),
]
