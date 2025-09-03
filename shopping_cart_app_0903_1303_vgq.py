# 代码生成时间: 2025-09-03 13:03:13
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Models
class Product(models.Model):
    """Represents a product that can be added to a shopping cart."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    """Represents a shopping cart."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    """Represents an item in a shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Views
class CartView(View):
    """Handles the shopping cart functionality."""
    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            items = cart.items.all()
            cart_items = [item.product.name for item in items]
            return JsonResponse({'items': cart_items, 'status': 'success'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Cart not found', 'status': 'error'})

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        try:
            product = Product.objects.get(id=product_id)
            if product.stock < quantity:
                messages.error(request, 'Not enough stock.')
                return redirect('cart')
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            product.stock -= quantity
            product.save()
            messages.success(request, 'Product added to cart.')
            return redirect('cart')
        except ObjectDoesNotExist:
            messages.error(request, 'Product not found.')
            return redirect('cart')
        except ValueError:
            messages.error(request, 'Invalid quantity.')
            return redirect('cart')

# URLs
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]

# Note: This is a simplified version of a shopping cart application. In a real-world scenario,
# you would need to handle authentication, permissions, and more complex cart logic such as
# removing items, updating quantities, and applying discounts.
