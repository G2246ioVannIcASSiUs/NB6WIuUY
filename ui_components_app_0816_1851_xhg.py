# 代码生成时间: 2025-08-16 18:51:41
Django application for a user interface component library.
This application provides models, views, and URLs
for managing and displaying UI components.
*/

"""
User Interface Components Application.

This Django app provides a basic framework for a UI component library.
It includes models for storing component information, views for
rendering component details, and URLs for routing requests.
"""

# Import necessary Django components
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import path
from django.views import View
from django.db import models

# Define the UI Component model
class UIComponent(models.Model):
    """Model representing a UI component."""
    name = models.CharField(max_length=255, help_text="The name of the UI component.")
    description = models.TextField(help_text="A brief description of the component.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the component was created.")

    class Meta:
        verbose_name = "UI Component"
        verbose_name_plural = "UI Components"

    def __str__(self):
        return self.name

# Define the UI Component detail view
class ComponentDetailView(View):
    """View for displaying a single UI component."""
    def get(self, request, *args, **kwargs):
        try:
            # Try to get the component by ID
            component_id = kwargs['component_id']
            component = UIComponent.objects.get(pk=component_id)
            # Render a template with the component details
            return render(request, 'ui_components/detail.html', {'component': component})
        except UIComponent.DoesNotExist:
            # Return a 404 error if the component does not exist
            raise Http404("UI Component does not exist.")

# Define the URL patterns for the UI component views
ui_component_patterns = [
    path('components/<int:component_id>/', ComponentDetailView.as_view(), name='component_detail'),
]

# Define the app configuration
class UIComponentsAppConfig(AppConfig):
    name = 'ui_components'
    verbose_name = "User Interface Components"