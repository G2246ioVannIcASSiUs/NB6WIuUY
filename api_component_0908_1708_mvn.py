# 代码生成时间: 2025-09-08 17:08:46
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Models
class Item(models.Model):
    """Model representing an item."""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Views
class ItemList(APIView):
    """API endpoint for listing and creating items."""
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """List all items in the database."""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create a new item."""
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):
    """API endpoint for retrieving, updating, and deleting an item."""
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Retrieve the item by its pk."""
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """Retrieve an item instance."""
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Update an item instance."""
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """Delete an item instance."""
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Serializers
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    """Serializer for item objects."""
    class Meta:
        model = Item
        fields = ('id', 'name', 'description')

# URLs
urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]
