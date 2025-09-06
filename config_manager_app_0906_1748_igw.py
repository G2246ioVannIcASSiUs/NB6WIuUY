# 代码生成时间: 2025-09-06 17:48:23
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# 配置文件管理器的模型
class Config(models.Model):
    """
    配置文件模型。
    """
    key = models.CharField(max_length=255, unique=True, help_text="配置键")
    value = models.TextField(help_text="配置值")
    description = models.TextField(blank=True, help_text="配置描述")

    def __str__(self):
        return f"{self.key} - {self.description}"

# 配置文件管理器的视图
class ConfigView(View):
    """
    提供配置文件的管理接口。
    """
    def get(self, request, *args, **kwargs):
        try:
            # 获取所有配置项
            config_items = Config.objects.all()
            configs = {item.key: item.value for item in config_items}
            return JsonResponse(configs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            # 添加或更新配置项
            key = request.POST.get('key')
            value = request.POST.get('value')
            description = request.POST.get('description', '')
            if key:
                config, created = Config.objects.get_or_create(key=key)
                config.value = value
                config.description = description
                config.save()
                return JsonResponse({'message': 'Config saved successfully', 'key': key, 'created': created})
            else:
                return JsonResponse({'error': 'Key is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # 错误处理示例，删除配置项
    def delete(self, request, *args, **kwargs):
        try:
            # 删除配置项
            key = request.POST.get('key')
            if key:
                Config.objects.filter(key=key).delete()
                return JsonResponse({'message': 'Config deleted successfully'})
            else:
                return JsonResponse({'error': 'Key is required'}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Config does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# 配置文件管理器的URL配置
urlpatterns = [
    path('config/', ConfigView.as_view(), name='config'),
]
