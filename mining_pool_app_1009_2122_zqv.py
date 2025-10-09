# 代码生成时间: 2025-10-09 21:22:43
# mining_pool_app
# This Django application manages the functionality of a mining pool.

# models.py
"""
Defines the database models for the mining pool application.
"""
from django.db import models


class MiningPool(models.Model):
    """
    Represents a mining pool.
    """
    name = models.CharField(max_length=100, help_text="The name of the mining pool.")
    description = models.TextField(blank=True, help_text="A description of the mining pool.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the mining pool was created.")

    def __str__(self):
        return self.name


# views.py
"""
Handles the logic of the views for the mining pool application.
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import MiningPool
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

@require_http_methods(["GET"])
def mining_pool_list(request):
    """
    Returns a list of mining pools.
    """
    mining_pools = MiningPool.objects.all()
    return JsonResponse(list(mining_pools.values()), safe=False)

@require_http_methods(["GET"])
def mining_pool_detail(request, pk):
    """
    Returns the details of a single mining pool.
    """
    try:
        mining_pool = MiningPool.objects.get(pk=pk)
        return JsonResponse(mining_pool.__dict__, safe=False)
    except ObjectDoesNotExist:
        return HttpResponse("Minig pool not found", status=404)

# urls.py
"""
Defines the URL patterns for the mining pool application.
"""
from django.urls import path
from .views import mining_pool_list, mining_pool_detail

app_name = 'mining_pool_app'

urlpatterns = [
    path('list/', mining_pool_list, name='mining_pool_list'),
    path('detail/<int:pk>/', mining_pool_detail, name='mining_pool_detail'),
]
