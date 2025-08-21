# 代码生成时间: 2025-08-21 21:23:53
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.files.storage import default_storage
from django.core.files.utils import FileProxyMixin
import os
import shutil
def get_valid_filename(s):
    # 确保文件名有效
    s = str(s).strip().replace('\', '/')  # 去除头尾空格并将反斜杠替换为斜杠
    return os.path.basename(s)  # 只保留文件名

class BulkRenameTool(View):
    @login_required
    def get(self, request, *args, **kwargs):
        # 显示批量重命名页面
        return render(request, 'bulk_rename_tool.html')

    @login_required
    def post(self, request, *args, **kwargs):
        files_to_rename = request.POST.getlist('files_to_rename[]')
        new_names = request.POST.getlist('new_names[]')

        if len(files_to_rename) != len(new_names):
            return JsonResponse({'error': '文件数量和新名称数量不匹配'}, status=400)

        for old_name, new_name in zip(files_to_rename, new_names):
            new_name = get_valid_filename(new_name)
            file_path = os.path.join(settings.MEDIA_ROOT, old_name)
            new_file_path = os.path.join(settings.MEDIA_ROOT, new_name)

            # 检查文件是否存在
            if not default_storage.exists(file_path):
                return JsonResponse({'error': f'文件 {old_name} 不存在'}, status=404)

            # 检查新文件名是否已存在
            if default_storage.exists(new_file_path):
                return JsonResponse({'error': f'文件名 {new_name} 已存在'}, status=400)

            try:
                default_storage.move(file_path, new_file_path)
            except Exception as e:
                return JsonResponse({'error': f'重命名文件时出错: {str(e)}'}, status=500)

        return JsonResponse({'message': '文件重命名成功'})

# urls.py
from django.urls import path
from .views import BulkRenameTool

urlpatterns = [
    path('bulk_rename_tool/', BulkRenameTool.as_view(), name='bulk_rename_tool'),
]

# models.py
# 该工具不需要model，因此不包含models.py

# bulk_rename_tool.html
<!-- 批量重命名工具的HTML模板 -->
<!DOCTYPE html>
<html>
<head>
    <title>批量文件重命名工具</title>
</head>
<body>
    <h1>批量文件重命名工具</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <label for="files_to_rename">选择文件:</label>
        <select name="files_to_rename[]" multiple>
            {% for file in files %}
                <option value="{{ file.name }}">{{ file.name }}</option>
            {% endfor %}
        </select>
        <label for="new_names">新名称:</label>
        <input type="text" name="new_names[]" required>
        <button type="submit">重命名</button>
    </form>
</body>
</html>