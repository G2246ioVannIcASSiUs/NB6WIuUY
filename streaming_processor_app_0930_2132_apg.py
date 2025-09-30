# 代码生成时间: 2025-09-30 21:32:09
# streaming_processor_app/models.py
from django.db import models


class DataStream(models.Model):
    """Model to store data streams."""
    stream_id = models.AutoField(primary_key=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DataStream {self.stream_id}"


# streaming_processor_app/views.py
from django.http import JsonResponse, HttpResponse
from .models import DataStream
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

@require_http_methods(['POST'])
def stream_data(request):
    """View to handle incoming data streams."""
    try:
        data = request.body.decode('utf-8')
        data_stream = DataStream(data=json.loads(data))
        data_stream.save()
        return JsonResponse({'status': 'success', 'message': 'Data stream processed.'}, status=201)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def error_404_view(request, exception):
    """Custom 404 error handler."""
    return HttpResponse('404 Not Found', status=404)


def error_500_view(request):
    """Custom 500 error handler."""
    return HttpResponse('500 Server Error', status=500)


# streaming_processor_app/urls.py
from django.urls import path
from .views import stream_data

urlpatterns = [
    path('stream/', stream_data, name='stream_data'),
]

# streaming_processor_app/apps.py
from django.apps import AppConfig

class StreamingProcessorAppConfig(AppConfig):
    """Django AppConfig for the StreamingProcessorApp."""
    name = 'streaming_processor_app'
