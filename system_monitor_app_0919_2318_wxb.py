# 代码生成时间: 2025-09-19 23:18:53
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
import psutil
import subprocess
import shutil
import os

# 定义一个性能监控模型
class SystemPerformance(models.Model):
    """
    存储系统性能数据
    """
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()
    network_usage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SystemPerformance at {self.timestamp}"

# 定义视图
def index(request):
    """
    首页视图
    """
    return render(request, 'system_monitor/index.html')

def performance_data(request):
    """
    获取系统性能数据的视图
    """
    try:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        # 获取内存使用率
        memory_usage = psutil.virtual_memory().percent
        # 获取磁盘使用率
        disk_usage = shutil.disk_usage('/').percent
        # 获取网络使用率
        network_stats = psutil.net_io_counters()
        network_usage = (network_stats.bytes_sent + network_stats.bytes_recv) / (1024 ** 3)  # GB

        # 存储性能数据
        performance = SystemPerformance(cpu_usage=cpu_usage, memory_usage=memory_usage, disk_usage=disk_usage, network_usage=network_usage)
        performance.save()

        return HttpResponse(f"CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%, Network: {network_usage}GB")
    except Exception as e:
        # 错误处理
        return HttpResponse(f"An error occurred: {e}", status=500)

# 定义URLs
from django.urls import path

urlpatterns = [
    path('monitor/', index, name='index'),
    path('performance/data/', performance_data, name='performance_data'),
]

# 确保该文件被Django识别为一个应用
default_app_config = 'system_monitor.apps.SystemMonitorConfig'