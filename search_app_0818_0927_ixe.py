# 代码生成时间: 2025-08-18 09:27:13
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import SearchItem

# Models
class SearchItem(models.Model):
    """Model for storing search items."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Views
@require_http_methods(['GET'])
def search(request):
    """View function to handle search requests.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        JsonResponse: A JSON response with search results.
    """
    try:
        query = request.GET.get('q')
        if not query:
            raise ValueError("No search query provided.")
        
        search_results = SearchItem.objects.filter(name__icontains=query)
        results = [{'name': item.name, 'description': item.description} for item in search_results]
        return JsonResponse({'results': results}, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'No items found.'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

# URLs
urlpatterns = [
    path('search/', search, name='search'),
]
