# 代码生成时间: 2025-09-04 17:52:13
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views import View
from django.urls import path
from .models import ScrapedPage

"""
A Django application component that implements a web content scraping tool.
This tool allows for retrieval and storage of webpage content.
"""

# Define models
class ScrapedPage(models.Model):
    '''Model to store scraped webpage contents.'''
    url = models.URLField(max_length=500, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''String representation of the ScrapedPage model.'''
        return f'{self.url}'

# Define views
class ScrapeWebPage(View):
    '''View to handle webpage scraping requests.'''
    def post(self, request, *args, **kwargs):
        '''Handle POST requests to scrape webpages.'''
        try:
            # Get the URL from the request data
            url = request.POST.get('url', '')
            if not url:
                return JsonResponse({'error': 'URL is required'}, status=400)

            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Store the scraped content in the ScrapedPage model
            scraped_page = ScrapedPage(url=url, content=str(soup))
            scraped_page.save()

            # Return a success response
            return JsonResponse({'message': 'Page scraped successfully', 'url': url}, status=200)
        except requests.RequestException as e:
            # Handle any request-related errors
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': 'An error occurred'}, status=500)

# Define URLs
urlpatterns = [
    path('scrape/', ScrapeWebPage.as_view(), name='scrape_web_page'),
]
