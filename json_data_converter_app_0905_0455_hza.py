# 代码生成时间: 2025-09-05 04:55:01
# json_data_converter_app/views.py
from django.http import JsonResponse
from django.views import View
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from .models import JsonDataModel
import json

"""
JSON Data Converter View
"""
class JsonDataConverter(View):
    """
    A view to convert JSON data into a structured Django model instance.
    """
    def post(self, request):
        """
        Converts incoming JSON data into a JsonDataModel instance and returns the instance in JSON format.
        """
        try:
            # Get the JSON data from the request body
            data = json.loads(request.body)
            # Create a new JsonDataModel instance with the data
            instance = JsonDataModel.objects.create(**data)
            # Serialize the instance to JSON using Django's JSONEncoder
            return JsonResponse(instance.__dict__, encoder=DjangoJSONEncoder)
        except ValidationError as e:
            # Handle validation errors from the model
            return JsonResponse({'error': str(e)}, status=400)
        except json.JSONDecodeError:
            # Handle JSON decoding errors
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

# json_data_converter_app/urls.py
from django.urls import path
from .views import JsonDataConverter

"""
URL patterns for JSON data converter app
"""
urlpatterns = [
    path('convert/', JsonDataConverter.as_view(), name='json-data-converter'),
]

# json_data_converter_app/models.py
from django.db import models

"""
JsonDataModel model for storing JSON data
"""
class JsonDataModel(models.Model):
    """
    A model to store JSON data.
    """
    # Assuming all fields are stored as strings for simplicity
    key1 = models.CharField(max_length=255)
    key2 = models.CharField(max_length=255)
    key3 = models.CharField(max_length=255)

    def __str__(self):
        return f"JsonDataModel(key1={self.key1}, key2={self.key2}, key3={self.key3})"