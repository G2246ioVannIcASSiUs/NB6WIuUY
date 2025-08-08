# 代码生成时间: 2025-08-09 01:06:57
from django.db import models
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import json

"""
A simple Django application to manage a blog with posts and comments.
"""

# models.py
class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Model representing a comment on a blog post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

# views.py
class PostListView(View):
    """View to list all blog posts."""
    def get(self, request):
        posts = Post.objects.all()
        data = [{'title': post.title, 'content': post.content, 'author': post.author.username} for post in posts]
        return HttpResponse(json.dumps(data), content_type='application/json')

class PostDetailView(View):
    """View to retrieve a specific blog post."""
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return HttpResponse(json.dumps({'title': post.title, 'content': post.content, 'author': post.author.username}), content_type='application/json')
        except Post.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'Post not found'}), content_type='application/json', status=404)

# urls.py
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
]
