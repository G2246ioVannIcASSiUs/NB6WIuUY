# 代码生成时间: 2025-08-22 07:06:22
from django.db import models
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging

# 设置日志配置
logger = logging.getLogger(__name__)


class ErrorLog(models.Model):
    """错误日志模型"""
    error_message = models.TextField(help_text="错误消息")
    created_at = models.DateTimeField(auto_now_add=True, help_text="创建时间")
    """
    记录一个错误信息到数据库
    """

def log_error(request):
    """
    记录错误日志的视图
    """
    if request.method == 'POST':
        try:
            error_message = request.POST.get('error_message', '')
            error_log = ErrorLog(error_message=error_message)
            error_log.save()
            logger.error(error_message)
            return HttpResponse("Error logged successfully")
        except Exception as e:
            logger.error(f"Error logging failed: {e}")
            return HttpResponse("Error logging failed", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)

def error_collector_urls():
    """
    返回错误日志收集器的URL配置
    """
    return [
        path('log_error/', require_http_methods(['POST'])(log_error), name='log_error'),
    ]


# 使该文件作为Django应用的组件独立运行时，可以进行简单的测试
if __name__ == '__main__':
    from django.conf.urls import url
    from django.conf import settings
    from django.core.management import execute_from_command_line
    settings.configure()
    execute_from_command_line(['', 'runserver'])
    urlpatterns = error_collector_urls()
    