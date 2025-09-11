# 代码生成时间: 2025-09-11 23:02:42
import re
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path

def clean_text(text):
    """Removes any non-alphanumeric characters from the input text."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

class DataCleaningView(View):
    """
    A Django view that provides data cleaning functionality.
    It expects a JSON payload with a 'text' key and returns
    the cleaned text.
    """
    def post(self, request, *args, **kwargs):
        """Processes the POST request to clean the provided text."""
        try:
            # Extract text from request payload
            data = request.POST
            text_to_clean = data.get('text', '')
            # Clean the text
            cleaned_text = clean_text(text_to_clean)
            # Return the cleaned text as a JSON response
            return JsonResponse({'cleaned_text': cleaned_text})
        except Exception as e:
            # Handle any errors that occur during text cleaning
            return JsonResponse({'error': str(e)}, status=400)

# Define the URL pattern for the DataCleaningView
urlpatterns = [
    path('clean/', DataCleaningView.as_view(), name='data_cleaning'),
]
