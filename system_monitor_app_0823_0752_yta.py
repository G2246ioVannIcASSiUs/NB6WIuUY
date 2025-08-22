# 代码生成时间: 2025-08-23 07:52:56
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.urls import path
import psutil
import os
import time

# 系统性能监控工具应用
class SystemMonitorApp:

    # 定义系统监控的指标
    class Metrics(models.Model):
        cpu_usage = models.FloatField()
        memory_usage = models.FloatField()
        disk_usage = models.FloatField()
        network_io = models.CharField(max_length=255)
        timestamp = models.DateTimeField(auto_now_add=True)
        """
        存储系统性能指标
        """"

        def __str__(self):
            return f"Metrics record {self.timestamp}"
    
    # 视图：获取系统性能指标
    class PerformanceView(View):
        def get(self, request):
            """
            获取当前系统的性能指标并返回
            返回值：
            - cpu_usage: float
            - memory_usage: float
            - disk_usage: float
            - network_io: str
            - timestamp: str
            """
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memory_usage = memory.percent
                disk = psutil.disk_usage('/')
                disk_usage = disk.percent
                network_io = f"{psutil.net_io_counters().bytes_sent} sent, {psutil.net_io_counters().bytes_recv} received"
                metrics = SystemMonitorApp.Metrics.objects.create(
                    cpu_usage=cpu_usage,
                    memory_usage=memory_usage,
                    disk_usage=disk_usage,
                    network_io=network_io
                )
                return JsonResponse(
                    {
                        "cpu_usage": cpu_usage,
                        "memory_usage": memory_usage,
                        "disk_usage": disk_usage,
                        "network_io": network_io,
                        "timestamp": metrics.timestamp.isoformat()
                    },
                    safe=False
                )
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    # URL配置
    def get_urls(self):
        """
        返回系统性能监控工具的URL配置
        """
        urlpatterns = [
            path('performance/', self.PerformanceView.as_view(), name='performance'),
        ]
        return urlpatterns
