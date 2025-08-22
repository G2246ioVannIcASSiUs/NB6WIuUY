# 代码生成时间: 2025-08-22 13:18:59
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import json
def get_next_status(order_status):
    # 这个函数用于根据当前订单状态返回下一个状态
    statuses = ['pending', 'processing', 'completed', 'canceled']
    index = statuses.index(order_status)
    if index < len(statuses) - 1:
        return statuses[index + 1]
    return None

class Order(models.Model):
    """Model to represent an order."""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    order_id = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.order_id
    
    def update_status(self, new_status):
        """Updates the order status."""
        if new_status in [status[0] for status in self.ORDER_STATUS_CHOICES]:
            self.status = new_status
            self.save()
        else:
            raise ValueError('Invalid order status')

class OrderView(View):
    """View to handle order operations."""
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """Handles POST requests to create a new order."""
        data = json.loads(request.body)
        try:
            order_id = data['order_id']
            customer_name = data['customer_name']
            amount = data['amount']
            order, created = Order.objects.get_or_create(
                order_id=order_id,
                defaults={'customer_name': customer_name, 'amount': amount}
            )
            if created:
                return JsonResponse({'message': 'Order created successfully', 'order_id': order_id}, status=201)
            else:
                return JsonResponse({'message': 'Order already exists'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def patch(self, request, *args, **kwargs):
        """Handles PATCH requests to update an order's status."""
        data = json.loads(request.body)
        try:
            order_id = data['order_id']
            new_status = data['new_status']
            order = Order.objects.get(order_id=order_id)
            order.update_status(new_status)
            return JsonResponse({'message': 'Order status updated successfully', 'new_status': new_status}, status=200)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# urls.py within the same Django app
urlpatterns = [
    path('orders/', OrderView.as_view(), name='order_view'),
]
