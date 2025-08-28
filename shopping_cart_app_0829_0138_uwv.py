# 代码生成时间: 2025-08-29 01:38:54
from django.db import models
from django.shortcuts import render, redirect
from django.views import View
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Models
class Product(models.Model):
    """ Model representing a product in the catalog. """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    """ Model representing a shopping cart. """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    
    def __str__(self):
        return f'Cart of {self.user.username}'
    
class CartItem(models.Model):
    """ Model representing an item in a shopping cart. """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

# Views
class CartView(View):
    """ View handling the shopping cart operations. """
    @login_required
    def get(self, request, *args, **kwargs):
        """
        Displays the user's cart contents.
        """
        user_cart = Cart.objects.get(user=request.user)
        cart_items = user_cart.products.all()
        cart_list = [{'product_name': item.name, 'quantity': CartItem.objects.get(cart=user_cart, product=item).quantity} for item in cart_items]
        return render(request, 'cart.html', {'cart_list': cart_list})
    
    def post(self, request, *args, **kwargs):
        """
        Adds a product to the cart or updates the quantity.
        """
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id)
            user_cart = Cart.objects.get(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except (ObjectDoesNotExist, ValueError):
            return JsonResponse({'error': 'Product not found or invalid quantity'}, status=400)
        
        return JsonResponse({'message': 'Product added/updated successfully.'})

    def delete(self, request, *args, **kwargs):
        """
        Removes a product from the cart.
        """
        product_id = request.POST.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
            user_cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=user_cart, product=product)
            cart_item.delete()
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'}, status=400)
        
        return JsonResponse({'message': 'Product removed from cart.'})

# URLs
urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
]

# Templates
# templates/cart.html
# {% extends "base.html" %}
# {% block content %}
#     <h2>Your Cart</h2>
#     <ul>
#         {% for item in cart_list %}
#             <li>{{ item.product_name }} - Quantity: {{ item.quantity }}</li>
#         {% endfor %}
#     </ul>
# {% endblock %}