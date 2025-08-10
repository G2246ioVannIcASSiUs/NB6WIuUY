# 代码生成时间: 2025-08-11 00:53:06
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist


# 订单状态枚举
class OrderStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    PROCESSING = 2, "Processing"
    SHIPPED = 3, "Shipped"
    COMPLETED = 4, "Completed"
    CANCELLED = 5, "Cancelled"

# 订单模型
class Order(models.Model):
    """订单信息模型"""
    customer_name = models.CharField(max_length=100)
    status = models.PositiveIntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} - {self.customer_name}"

# 订单视图
class OrderProcessView(View):
    """订单处理视图"""
    @require_http_methods(['GET', 'POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # 创建新订单
    def post(self, request, *args, **kwargs):
        """创建新订单"""
        customer_name = request.POST.get("customer_name")
        if not customer_name:
            return JsonResponse({'error': 'Customer name is required'}, status=400)

        order = Order.objects.create(customer_name=customer_name)
        return JsonResponse({'id': order.pk, 'status': order.status}, status=201)

    # 更新订单状态
    def patch(self, request, order_id):
        """更新订单状态"""
        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        status = request.POST.get("status")
        if status and status in [s[0] for s in OrderStatus.choices]:
            order.status = int(status)
            order.save()
            return JsonResponse({'status': order.status}, status=200)
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)

# 订单URL配置
urlpatterns = [
    path('orders/', OrderProcessView.as_view(), name='order_process'),
]
