# 代码生成时间: 2025-09-05 17:20:50
import datetime
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


# Models
class Order(models.Model):
    """
    A model representing an order.
    """
    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')])

    def __str__(self):
        return f"{self.customer_name} - {self.product_name} - {self.quantity}"


# Views
class OrderCreateView(View):
    """
    A view to create a new order.
    """
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        try:
            data = request.POST
            customer_name = data.get('customer_name')
            product_name = data.get('product_name')
            quantity = int(data.get('quantity'))
            
            # Validation
            if not all([customer_name, product_name, quantity]):
                raise ValueError("Missing required data.")
            
            # Create Order
            order = Order(
                customer_name=customer_name,
                product_name=product_name,
                quantity=quantity,
                status='pending'
            )
            order.save()
            
            # Return success response
            return JsonResponse({'message': 'Order created successfully.', 'order_id': order.id}, status=201)
        except (ValueError, TypeError, ValidationError) as e:
            return JsonResponse({'error': str(e)}, status=400)


# URL Configuration
urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order_create'),
]
