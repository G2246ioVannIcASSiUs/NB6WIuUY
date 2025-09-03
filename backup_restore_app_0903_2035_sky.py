# 代码生成时间: 2025-09-03 20:35:45
import os
from datetime import datetime
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.conf import settings
from django.core.management import call_command
import tarfile
import shutil

# 数据备份模型
class Backup(models.Model):
    """ 数据备份记录模型 """
    filename = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    size = models.BigIntegerField()
    backup_type = models.CharField(max_length=50)

    def __str__(self):
        return self.filename

# 数据备份视图
class DataBackupView(View):
    """ 数据备份视图 """
    def post(self, request, *args, **kwargs):
        "