# 代码生成时间: 2025-08-21 03:55:52
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.exceptions import ImproperlyConfigured
from .models import Theme
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

"""
Theme switcher application enabling users to switch themes.

This application allows authenticated users to switch between different themes.
Themes are stored in the database and associated with the user's profile.
"""


class ThemeSwitcherView(View):
    """
    A view to switch the user's theme.

    This view handles GET requests to switch themes and updates the user's
    theme preference in the session.
    """

    @method_decorator(login_required, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @require_GET
    def get(self, request):
        try:
            theme_name = request.GET.get('theme')
            if not theme_name:
                messages.error(request, 'No theme provided.')
                return redirect('home')

            # Validate theme exists in the database
            theme = Theme.objects.get(name__iexact=theme_name)
            request.session['theme'] = theme.name
            messages.success(request, 'Theme switched successfully.')
            return redirect('home')
        except Theme.DoesNotExist:
            messages.error(request, 'Theme does not exist.')
            return HttpResponseBadRequest('Theme does not exist.')
        except Exception as e:
            messages.error(request, 'An error occurred.')
            return HttpResponseBadRequest(str(e))


# Models
class Theme(models.Model):
    """
    A model representing a theme.

    Each theme has a unique name and may have other attributes such as color scheme.
    """
    name = models.CharField(max_length=100, unique=True)
    # Add more fields as needed

    def __str__(self):
        return self.name


# URLs
# urlpatterns = [
#     path('switch_theme/', ThemeSwitcherView.as_view(), name='switch_theme'),
# ]