# 代码生成时间: 2025-09-28 17:46:57
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


# Models
class EnergyDevice(models.Model):
    """Model representing an energy device."""
    name = models.CharField(max_length=255, help_text="The name of the device.")
    type = models.CharField(max_length=100, help_text="The type of the device.")
    energy_consumption = models.FloatField(help_text="The current energy consumption in watts.")

    def __str__(self):
        return self.name


# Views
@method_decorator(csrf_exempt, name='dispatch')
class EnergyDeviceView(View):
    "