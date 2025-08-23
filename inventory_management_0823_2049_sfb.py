# 代码生成时间: 2025-08-23 20:49:01
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.urls import path


# Model for Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    """A model representing a product in the inventory system."""
    def __str__(self):
        return self.name


# View for Product
class ProductView(View):
    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.all()
            return JsonResponse([{'name': product.name, 'quantity': product.quantity} for product in products], safe=False)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name')
            quantity = int(request.POST.get('quantity'))
            description = request.POST.get('description')
            product = Product.objects.create(name=name, quantity=quantity, description=description)
            return JsonResponse({'id': product.id, 'name': product.name, 'quantity': product.quantity}, status=201)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
            name = request.POST.get('name', product.name)
            quantity = int(request.POST.get('quantity', product.quantity))
            description = request.POST.get('description', product.description)
            product.name = name
            product.quantity = quantity
            product.description = description
            product.save()
            return JsonResponse({'id': product.id, 'name': product.name, 'quantity': product.quantity})
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return HttpResponse(status=204)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# URL patterns for Product
urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:pk>/', ProductView.as_view(), name='product-detail'),
]

"""
This Django application component represents a simple inventory management system.
It includes a Product model, a ProductView for handling HTTP requests,
and URL patterns for routing requests to ProductView."""