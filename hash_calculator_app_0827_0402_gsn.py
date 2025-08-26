# 代码生成时间: 2025-08-27 04:02:00
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import hashlib

"""
哈希值计算工具应用组件
提供哈希值计算功能，支持SHA256, SHA384, SHA512算法
"""


# models.py
# 由于这个应用组件不需要持久化存储数据，所以不需要定义模型


# views.py
class HashCalculatorView(View):
    """
    哈希值计算视图
    提供一个HTTP接口，用于计算字符串的哈希值
# FIXME: 处理边界情况
    """

    def post(self, request):
        # 获取请求体中的字符串
        try:
            data = request.POST.get('string')
            if data is None:
                return JsonResponse({'error': 'Missing string parameter'}, status=400)

            # 计算哈希值
            hash_algorithm = request.POST.get('algorithm', 'sha256')
            if hash_algorithm not in ['sha256', 'sha384', 'sha512']:
                return JsonResponse({'error': 'Invalid algorithm'}, status=400)

            if hash_algorithm == 'sha256':
                hash_object = hashlib.sha256()
            elif hash_algorithm == 'sha384':
                hash_object = hashlib.sha384()
            else:
                hash_object = hashlib.sha512()

            hash_object.update(data.encode())
            hash_value = hash_object.hexdigest()

            return JsonResponse({'hash': hash_value})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
# 扩展功能模块


# urls.py
urlpatterns = [
    path('calculate-hash/', HashCalculatorView.as_view(), name='calculate-hash'),
]
