# 代码生成时间: 2025-09-18 20:58:21
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist


"""
配置文件管理器应用组件，遵循Django最佳实践，实现配置文件的CRUD操作。
"""

# models.py
class Config(models.Model):
    """
    配置文件模型
    """
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


# views.py
class ConfigListView(View):
    """
    获取所有配置项
    """
    def get(self, request):
        configs = Config.objects.all().values('key', 'value')
        return JsonResponse(list(configs), safe=False)

class ConfigDetailView(View):
    """
    获取指定配置项
    """
    def get(self, request, key):
        try:
            config = Config.objects.get(key=key)
            return JsonResponse({'key': config.key, 'value': config.value})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Config not found'}, status=404)

class ConfigCreateView(View):
    """
    创建配置项
    """
    def post(self, request):
        key = request.POST.get('key')
        value = request.POST.get('value')
        if not key or not value:
            return JsonResponse({'error': 'Key and value are required'}, status=400)
        Config.objects.create(key=key, value=value)
        return JsonResponse({'key': key, 'value': value}, status=201)

class ConfigUpdateView(View):
    """
    更新配置项
    """
    def put(self, request, key):
        try:
            config = Config.objects.get(key=key)
            config.value = request.POST.get('value')
            config.save()
            return JsonResponse({'key': key, 'value': config.value})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Config not found'}, status=404)

class ConfigDeleteView(View):
    """
    删除配置项
    """
    def delete(self, request, key):
        try:
            Config.objects.get(key=key).delete()
            return JsonResponse({'message': 'Config deleted'}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Config not found'}, status=404)

# urls.py
config_patterns = [
    path('configs/', ConfigListView.as_view(), name='config_list'),
    path('configs/<str:key>/', ConfigDetailView.as_view(), name='config_detail'),
    path('configs/create/', ConfigCreateView.as_view(), name='config_create'),
    path('configs/<str:key>/update/', ConfigUpdateView.as_view(), name='config_update'),
    path('configs/<str:key>/delete/', ConfigDeleteView.as_view(), name='config_delete'),
]

# 在app的urls.py中引入config_patterns
from django.urls import include

urlpatterns = [
    path('config/', include('config_manager_app.urls')),
]
