# 代码生成时间: 2025-09-05 23:11:28
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Models
class Product(models.Model):
    """Model representing a product that can be added to the cart."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


class Cart(models.Model):
    """Model representing a shopping cart."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartItem(models.Model):
    """Model representing an item in the shopping cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

# Views
@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart."""
    try:
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Added {product.name} to your cart.")
    except Product.DoesNotExist:
        messages.error(request, f"Product {product_id} does not exist.")
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    """Display the user's cart details."""
    try:
        cart = Cart.objects.get(user=request.user)
        total = sum(item.product.price * item.quantity for item in cart.items.all())
        return render(request, 'cart_detail.html', {'cart': cart, 'total': total})
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the user's cart."""
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
        messages.success(request, f"Removed {item.product.name} from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, f"Item {item_id} does not exist in your cart.")
    return redirect('cart_detail')

# URLs
urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('detail/', cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]
