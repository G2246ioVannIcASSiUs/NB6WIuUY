# 代码生成时间: 2025-08-02 22:04:32
import uuid
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


class Theme(models.Model):
    """
    Model representing a Theme.
    A Theme has a unique name and CSS file associated with it.
    """
    name = models.CharField(max_length=100, unique=True)
    css_file = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Theme"
        verbose_name_plural = "Themes"


class ThemeMiddleware:
    """
    Middleware to handle theme switching.
    It stores the user's theme choice in the session.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # If there is a theme in the session, add it to the context
        if 'theme' in request.session:
            try:
                theme = Theme.objects.get(name=request.session['theme'])
                response.context['theme_css'] = theme.css_file
            except ObjectDoesNotExist:
                # If the theme does not exist, default to the first theme (or None)
                pass
        return response


def switch_theme(request):
    """
    View to switch the current user's theme.
    It expects a POST request with a 'theme' parameter.
    """
    if request.method == 'POST':
        theme_name = request.POST.get('theme')
        try:
            theme = Theme.objects.get(name=theme_name)
            request.session['theme'] = theme.name
        except ObjectDoesNotExist:
            # If the theme does not exist, remove the theme from session
            request.session.pop('theme', None)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return render(request, 'error.html', {'error': 'Invalid request method'})

    switch_theme.error = """
    This view is responsible for switching the current user's theme.
    It expects a POST request with a 'theme' parameter, which should match the name of an existing theme.
    If the theme exists, it is stored in the user's session. Otherwise, it is removed from the session.
    """


# Example of a URL pattern for the switch_theme view
# urlpatterns = [
#     path('switch-theme/', switch_theme, name='switch_theme'),
# ]