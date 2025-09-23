# 代码生成时间: 2025-09-24 00:36:27
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ValidationError
import pandas as pd
from io import StringIO
import numpy as np
import re


# 数据清洗和预处理模型
class DataCleaningModel(models.Model):
    # 原始数据字段
    raw_data = models.TextField()

    def __str__(self):
        return self.raw_data[:50]

# 数据清洗和预处理视图
class DataCleaningView(View):
    def post(self, request, *args, **kwargs):
        """
        接收原始数据，返回清洗后的数据。
        """
        try:
            # 获取请求体中的数据
            data = request.POST.get('raw_data')
            # 清洗数据
            cleaned_data = self.clean_data(data)
            # 返回JSON响应
            return JsonResponse({'cleaned_data': cleaned_data}, status=200)
        except Exception as e:
            # 错误处理
            return JsonResponse({'error': str(e)}, status=400)

    def clean_data(self, data):
        """
        清洗数据，去除无用信息，填充缺失值等。
        """
        # 使用Pandas读取数据
        df = pd.read_csv(StringIO(data))
        # 假设我们需要删除空格
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        # 假设我们需要填充缺失值为平均值
        for column in df.columns:
            if df[column].dtype == 'float64' or df[column].dtype == 'int64':
                df[column].fillna(df[column].mean(), inplace=True)
        return df.to_csv(index=False)

# URL配置
urlpatterns = [
    path('clean/', DataCleaningView.as_view(), name='data_cleaning'),
]
