# 代码生成时间: 2025-08-01 08:05:31
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import renderers

# Models
class ExampleModel(models.Model):
    """
    An example model for demonstration purposes.
    """
    name = models.CharField(max_length=100)
    data = models.TextField()

    def __str__(self):
        return self.name

# Views
class ExampleAPIView(APIView):
    """
    A simple APIView to handle GET and POST requests for the ExampleModel.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, format=None):
        """
        List all example instances.
        """
        example_list = ExampleModel.objects.all()
        serializer = ExampleSerializer(example_list, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Create a new example instance.
        """
        serializer = ExampleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Serializers
from rest_framework import serializers

class ExampleSerializer(serializers.ModelSerializer):
    """
    Serializer for ExampleModel instances.
    """
    class Meta:
        model = ExampleModel
        fields = '__all__'

# URLs
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'examples', ExampleAPIView)

urlpatterns = [
    path('', include(router.urls)),
]

# Error Handling
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """
    Custom exception handler to return a more informative error response.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    if response is not None:
        # Now add the HTTP status code to our response.
        response.data['status_code'] = response.status_code
        return Response(response.data, status=response.status_code)
    
    # If REST framework handled the exception, then return the response.
    # If not, then re-raise the exception.
    return response

# Update Django's default exception handler.
# You need to import this in your settings.py file.
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'your_app_name.custom_exception_handler',
}