# 代码生成时间: 2025-09-23 00:47:24
{
    "__init__.py": """
    theme_switcher_app
    ----------------
    This Django app provides functionality for handling theme switching
    within a Django project.
    """

    # nothing to see here, move along...
    
    ",
    "models.py": """
    from django.db import models
    from django.contrib.auth.models import User

    # Create your models here.

    class Theme(models.Model):
        """Model representing themes available in the application."""
        name = models.CharField(max_length=100, unique=True)
        description = models.TextField(blank=True, null=True)

        def __str__(self):
            return self.name
    
    """,
    "views.py": """
    from django.shortcuts import render, redirect
    from django.contrib.auth.decorators import login_required
    from django.contrib import messages
    from .models import Theme
    from django.utils.decorators import method_decorator
    from django.views import View

    class ThemeSwitcher(View):
        """
        A class-based view to switch user's theme.
        """
        def post(self, request, *args, **kwargs):
            # Get the currently logged in user
            user = request.user
            if not user.is_authenticated:
                # Not authorized, redirect to login page
                return redirect('login')
            
            # Get the theme from the request body
            theme_name = request.POST.get('theme', None)
            
            if theme_name and Theme.objects.filter(name=theme_name).exists():
                # Update the user's preferred theme
                user.profile.theme = theme_name
                user.profile.save()
                
                # Success message
                messages.success(request, 'Theme switched successfully.')
            else:
                # Error message
                messages.error(request, 'Invalid theme selected.')
            
            # Redirect back to the previous page
            return redirect('home')
    
    """,
    