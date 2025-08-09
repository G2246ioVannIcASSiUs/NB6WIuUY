# 代码生成时间: 2025-08-10 01:17:59
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

"""
Inventory Management App: handles the operations for a stock management system.
"""

# Define models for the Inventory Management System
class Product(models.Model):
    """
    Model representing a product in the inventory.
    """
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (Quantity: {self.quantity})"

# View for handling Inventory Management operations
@method_decorator(csrf_exempt, name='dispatch')
class InventoryManagementView(View):
    """
    View for handling inventory management operations.
    Provides endpoints for managing products in the inventory.
    """
    def get(self, request):
        """
        Retrieves all products from the inventory.
        """
        products = Product.objects.all()
        return JsonResponse(list(products.values()), safe=False)

    def post(self, request):
        """
        Adds a new product to the inventory.
        """
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity', 0))
        price = float(request.POST.get('price', '0.00'))
        product = Product(name=name, quantity=quantity, price=price)
        try:
            product.save()
            return JsonResponse({'message': 'Product added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk):
        """
        Updates a product in the inventory by its primary key.
        """
        product = Product.objects.get(pk=pk)
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity', product.quantity))
        price = float(request.POST.get('price', str(product.price)))
        product.name = name
        product.quantity = quantity
        product.price = price
        try:
            product.save()
            return JsonResponse({'message': 'Product updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    def delete(self, request, pk):
        "