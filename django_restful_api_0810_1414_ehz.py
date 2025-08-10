# 代码生成时间: 2025-08-10 14:14:35
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

# Define the model
class Item(models.Model):
    """ Model for storing items. """
    name = models.CharField(max_length=100, help_text="Name of the item.")
    description = models.TextField(help_text="Description of the item.")

    def __str__(self):
        return self.name

# Define the serializer
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    """ Serializer for the Item model. """
    class Meta:
        model = Item
        fields = '__all__'

# Define the API View
class ItemAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any client to access this view
    """ API View for handling Item resources. """
    def get(self, request):
        """ Get all items. """
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    @method_decorator(csrf_exempt)  # Allow cross-site requests
    def post(self, request):
        """ Create a new item. """
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define the URL patterns
urlpatterns = [
    path('items/', ItemAPIView.as_view(), name='item-list'),
]

# Alternatively, using a ViewSet for a more RESTful approach
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    "