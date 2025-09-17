# 代码生成时间: 2025-09-18 02:04:53
from django.conf.urls import url
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import json


class Product(models.Model):
    """Model representing a product in the store."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Model representing a shopping cart."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Model representing an item in a shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class CartView(View):
    """View responsible for handling cart operations."""
    def post(self, request, *args, **kwargs):
        try:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(pk=product_id)
            
            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'status': 'success', 'message': 'Product added to cart.'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product or cart not found.'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid product ID or quantity.'})

    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            
            # Create a dictionary to hold cart data
            cart_data = {'items': []}
            for item in cart_items:
                cart_data['items'].append({'product_name': item.product.name, 'quantity': item.quantity})
            return JsonResponse(cart_data)
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart not found.'})


# URL configuration for cart operations
urlpatterns = [
    url(r'^cart/$', CartView.as_view(), name='cart_view'),
]
