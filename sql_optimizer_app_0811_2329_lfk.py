# 代码生成时间: 2025-08-11 23:29:09
from django.db import models, transaction
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# Models
class Query(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    query = models.TextField()
    optimized_query = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Views
@require_http_methods(['GET', 'POST'])
def optimize_query_view(request):
    try:
        # Handle POST request to optimize query
        if request.method == 'POST':
            query_data = request.POST
            query = query_data.get('query')
            # Call optimize_query function to optimize the given query
            optimized_query = optimize_query(query)
            data = {'optimized_query': optimized_query}
            return JsonResponse(data, safe=False)
        
        # Handle GET request to show all queries
        queries = Query.objects.all().values('id', 'name', 'description', 'query')
        data = list(queries)
        return JsonResponse(data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def optimize_query(query):
    