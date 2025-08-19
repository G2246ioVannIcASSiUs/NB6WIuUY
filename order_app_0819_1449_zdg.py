# 代码生成时间: 2025-08-19 14:49:42
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods

# Models
class Order(models.Model):
    """Order model to represent an order."""
    customer_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

# Views
@require_http_methods(["GET"])
def order_list(request):
    """View to list all orders."""
    orders = Order.objects.all()
    return JsonResponse(list(orders.values()), safe=False)

@require_http_methods(["POST"])
def order_create(request):
    """View to create a new order."""
    try:
        data = request.POST
        order = Order(
            customer_name=data.get("customer_name"),
            total_amount=data.get("total_amount")
        )
        order.save()
        return JsonResponse({
            "message": "Order created successfully",
            "order_id": order.id,
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "error": str(e),
        }, status=400)

# Urls
urlpatterns = [
    path("orders/", order_list, name="order_list"),
    path("orders/create/", order_create, name="order_create"),
]
