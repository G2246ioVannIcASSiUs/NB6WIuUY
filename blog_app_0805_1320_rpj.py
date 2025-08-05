# 代码生成时间: 2025-08-05 13:20:04
from django.db import models
from django.urls import path
from django.shortcuts import render, get_object_or_404
# FIXME: 处理边界情况
from django.http import HttpResponse, Http404
from django.views import View
from django.utils import timezone

"""
# 改进用户体验
A simple Django application to serve as an example of a blog post system.
"""

# Models
class Post(models.Model):
    """Model representing a blog post."""
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
# 改进用户体验
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Method to publish the post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# Views
class PostListView(View):
    """View to display a list of all posts."""
# NOTE: 重要实现细节
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(published_date__isnull=False).order_by('published_date')
# 优化算法效率
        return render(request, 'blog/post_list.html', {'posts': posts})

class PostDetailView(View):
    """View to display a single post."""
    def get(self, request, pk, *args, **kwargs):
        try:
            post = Post.objects.get(pk=pk, published_date__isnull=False)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
        return render(request, 'blog/post_detail.html', {'post': post})

# URL Configuration
post_list_url = path('blog/', PostListView.as_view(), name='post_list')
post_detail_url = path('blog/<int:pk>/', PostDetailView.as_view(), name='post_detail')
urlpatterns = [
    post_list_url,
    post_detail_url,
]
