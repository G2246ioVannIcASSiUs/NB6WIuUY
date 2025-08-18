# 代码生成时间: 2025-08-18 19:19:18
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.conf import settings
import os
import re
from django.views import View

"""
批量文件重命名工具，用于Django应用中。
使用此工具时，需确保传入的文件路径在settings.MEDIA_ROOT下，
且有相应的权限操作文件。
"""

class BulkRenameTool(View):
    @require_http_methods(['POST'])
    def post(self, request, *args, **kwargs):
        try:
            # 获取请求中的文件路径和新文件名模式
            file_paths = request.POST.getlist('file_paths')
            new_name_pattern = request.POST.get('new_name_pattern')

            # 检查文件路径是否在MEDIA_ROOT下
            if not all(os.path.commonprefix([path, settings.MEDIA_ROOT]) == settings.MEDIA_ROOT for path in file_paths):
                raise ValidationError('所有文件路径必须在MEDIA_ROOT目录下。')

            # 检查文件名模式是否为有效的正则表达式
            if not re.match(new_name_pattern, 'test'):
                raise ValidationError('新的文件名模式无效。')

            # 执行文件重命名操作
            for path in file_paths:
                # 检查文件是否存在
                if not os.path.exists(path):
                    raise FileNotFoundError(f'文件 {path} 不存在。')

                # 构造新文件名
                new_name = re.sub(r'\d+', str(len([file for file in os.listdir(os.path.dirname(path)) if re.match(new_name_pattern, file)])), new_name_pattern)
                new_path = os.path.join(os.path.dirname(path), new_name)

                # 重命名文件
                os.rename(path, new_path)

            return JsonResponse({'message': '文件重命名成功。'})

        except ValidationError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except FileNotFoundError as fnfe:
            return JsonResponse({'error': str(fnfe)}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# urls.py
# from django.urls import path
# from .views import BulkRenameTool

# urlpatterns = [
#     path('bulk_rename/', BulkRenameTool.as_view(), name='bulk_rename_tool'),
# ]
