# 代码生成时间: 2025-08-29 23:35:42
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
import logging
import re
import json
from datetime import datetime

# Django应用的配置类
class LogParserAppConfig:
    default_auto_field = 'django.db.models.BigAutoField'

# Django模型类，用于存储日志解析结果
class LogEntry(models.Model):
    """Log entry model to store the parsed log data."""
    line_number = models.IntegerField(help_text='The line number in the log file.')
    timestamp = models.DateTimeField(help_text='The timestamp of the log entry.')
    log_level = models.CharField(max_length=10, help_text='The log level of the entry.')
    message = models.TextField(help_text='The message contained in the log entry.')
    
    def __str__(self):
        return f'{self.timestamp} - {self.log_level}: {self.message}'

    class Meta:
        verbose_name_plural = 'Log Entries'

# Django视图函数，解析日志文件
def parse_log_file(request):
    """ Parse a log file and store the results in the database. """
    # 错误处理
    if request.method != 'POST':
        return HttpResponse('Invalid request method.', status=405)
    
    file = request.FILES.get('logfile')
    if not file:
        return HttpResponse('No file provided.', status=400)
    
    try:
        log_entries = []
        with file.open('r') as f:
            for line_number, line in enumerate(f, start=1):
                # 使用正则表达式匹配日志条目
                match = re.search(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\w+) (.+)', line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                    log_entries.append(LogEntry(
                        line_number=line_number,
                        timestamp=timestamp,
                        log_level=log_level,
                        message=message
                    ))
        LogEntry.objects.bulk_create(log_entries)
        return HttpResponse('Log file parsed successfully.', status=200)
    except Exception as e:
        logging.error(f'Error parsing log file: {e}')
        return HttpResponse('Error parsing log file.', status=500)

# Django URL配置
app_name = 'log_parser'
urlpatterns = [
    path('parse/', parse_log_file, name='parse_log'),
]

# 示例模板（如果需要）
# log_parser.html:
# <!DOCTYPE html>
# <html lang="en">\# <head>
#     <meta charset="UTF-8">\#     <title>Log Parser</title>
# </head>
# <body>
#     <h1>Upload Log File</h1>
#     <form method="post" enctype="multipart/form-data">
#         {% csrf_token %}
#         <input type="file" name="logfile" required>
#         <button type="submit">Parse Log</button>
#     </form>
# </body>
# </html>