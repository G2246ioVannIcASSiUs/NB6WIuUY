# 代码生成时间: 2025-07-31 05:58:49
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import path
from django.views import View

# Models
class CustomUser(User):
    """ Custom user model that extends Django's built-in User model. """
    pass

# Views
class UserLoginView(View):
    """ View to handle user login. """
    def get(self, request):
        """ Render the login page. """
        return render(request, 'login.html')

    def post(self, request):
        """ Handle the login form submission. """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

# URLs
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]

# Templates
# login.html
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Login</title>
# </head>
# <body>
#     {% if messages %}
#         {% for message in messages %}
#             <p>{{ message }}</p>
#         {% endfor %}
#     {% endif %}
#     <form method="post" action="{% url 'login' %}">
#         {% csrf_token %}
#         Username: <input type="text" name="username" required>
#         Password: <input type="password" name="password" required>
#         <input type="submit" value="Login">
#     </form>
# </body>
# </html>