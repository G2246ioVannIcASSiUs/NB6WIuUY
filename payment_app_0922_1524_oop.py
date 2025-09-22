# 代码生成时间: 2025-09-22 15:24:21
from django.conf.urls import url
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

# Models

class Payment(models.Model):
    """ Model to store payment details. """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} by {self.user.username}"

# Views

@require_http_methods(['POST'])
def process_payment(request):
    """
    Process a payment.
    
    Args:
        request (HttpRequest): The Django HTTP request object.
        
    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    try:
        user_id = request.POST.get('user_id')
        amount = request.POST.get('amount')
        status = request.POST.get('status', 'pending')

        if not all([user_id, amount]):
            return HttpResponseBadRequest('Missing required payment information.')

        user = request.user
        if not user.is_authenticated:
            return HttpResponseBadRequest('User authentication required.')

        # Validate user_id and amount
        if not user_id.isdigit() or not amount.replace('.', '', 1).isdigit():
            return HttpResponseBadRequest('Invalid user_id or amount.')

        Payment.objects.create(user_id=user_id, amount=amount, status=status)
        return JsonResponse({'message': 'Payment processed successfully.'})
    except IntegrityError as e:
        return HttpResponseBadRequest('Database error occurred.')
    except Exception as e:
        return HttpResponseBadRequest('An unexpected error occurred.')

# URLs

urlpatterns = [
    url(r'^process/$', process_payment, name='process_payment'),
]
