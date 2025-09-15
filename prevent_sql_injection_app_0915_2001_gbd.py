# 代码生成时间: 2025-09-15 20:01:39
from django.db import models, IntegrityError
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.db.models import Q
import json

# Model for demonstration purposes
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

# View to demonstrate prevention of SQL injection
class ProductListView(View):
    """
    A view to list products with safety checks to prevent SQL injection.
    """
    def get(self, request, *args, **kwargs):
        try:
            search_query = request.GET.get('search', '')
            # Using Django's ORM to build a safe query
            products = Product.objects.filter(name__icontains=search_query)
            product_list = list(products.values('name', 'price'))
            return JsonResponse({'products': product_list}, safe=False)
        except IntegrityError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            # Generic error handling
            return JsonResponse({'error': 'An error occurred'}, status=500)

# URL configuration
urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
]
