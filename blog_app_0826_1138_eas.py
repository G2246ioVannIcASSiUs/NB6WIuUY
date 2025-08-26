# 代码生成时间: 2025-08-26 11:38:11
from django.db import models
from django.core.validators import MinLengthValidator
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
# 扩展功能模块
from django.contrib.auth.decorators import login_required

"""
# 增强安全性
A simple Django application that manages a blog post system.
This application includes models for authors and blog posts, views for listing and viewing posts,
and URL configurations for the application.
"""

class Author(models.Model):
    """
    Model representing an author.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
# NOTE: 重要实现细节
    
    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model representing a blog post.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField(validators=[MinLengthValidator(10)])
# 增强安全性
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
# 增强安全性
        ordering = ['-created_on']

"""
# 改进用户体验
Views for the blog application.
"""
# 增强安全性
class PostListView(ListView):
    """
    View for listing all blog posts.
# 添加错误处理
    """
    model = Post
    template_name = 'blog/post_list.html'
# 添加错误处理
    context_object_name = 'posts'
    
class PostDetailView(View):
    """
    View for viewing a single blog post.
    """
# NOTE: 重要实现细节
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
        return render(request, 'blog/post_detail.html', {'post': post})

"""
# 扩展功能模块
URL configurations for the blog application.
"""
# TODO: 优化性能
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
# 扩展功能模块
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
