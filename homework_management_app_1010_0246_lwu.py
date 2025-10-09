# 代码生成时间: 2025-10-10 02:46:28
from django.db import models


# Create your models here.
class Homework(models.Model):
    # Fields for the Homework model
    title = models.CharField(max_length=200, help_text="Enter the title of the homework")
    description = models.TextField(help_text="Enter a brief description of the homework")
    due_date = models.DateTimeField(help_text="Enter the due date for the homework")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


/homework_management_app/views.py
"""
Define the views for the homework management app.
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Homework

# Create your views here.
def homework_list(request):
    """
    A view to display a list of all homework assignments.
    """
    homeworks = Homework.objects.all()
    return render(request, 'homework_list.html', {'homeworks': homeworks})


def homework_detail(request, pk):
    """
    A view to display the details of a specific homework assignment.
    """
    homework = get_object_or_404(Homework, pk=pk)
    return render(request, 'homework_detail.html', {'homework': homework})


def homework_create(request):
    """
    A view to create a new homework assignment.
    """
    if request.method == 'POST':
        Homework.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date']
        )
        return HttpResponseRedirect(reverse('homework_list'))
    return render(request, 'homework_form.html')

/homework_management_app/urls.py
"""
Define the URL patterns for the homework management app.
"""
from django.urls import path
from . import views

app_name = 'homework_management_app'

urlpatterns = [
    # URL pattern for the homework list view
    path('', views.homework_list, name='homework_list'),
    # URL pattern for the homework detail view
    path('<int:pk>/', views.homework_detail, name='homework_detail'),
    # URL pattern for the homework create view
    path('create/', views.homework_create, name='homework_create'),
]

/homework_management_app/templates/homework_list.html
{% extends "base.html" %}
{% block content %}
<h2>Homework List</h2>
<ul>
    {% for homework in homeworks %}
    <li>{{ homework.title }} - Due: {{ homework.due_date }}</li>
    {% endfor %}
</ul>
<a href="{% url 'homework_management_app:homework_create' %}">Create New Homework</a>
{% endblock %}

/homework_management_app/templates/homework_detail.html
{% extends "base.html" %}
{% block content %}
<h2>{{ homework.title }}</h2>
<p>{{ homework.description }}</p>
<p>Due: {{ homework.due_date }}</p>
<a href="{% url 'homework_management_app:homework_list' %}">Back to List</a>
{% endblock %}

/homework_management_app/templates/homework_form.html
{% extends "base.html" %}
{% block content %}
<h2>Create New Homework</h2>
<form method="post">{% csrf_token %}
    Title: <input type="text" name="title" required><br>
    Description: <textarea name="description" required></textarea><br>
    Due Date: <input type="datetime-local" name="due_date" required><br>
    <input type="submit" value="Create">
</form>
{% endblock %}