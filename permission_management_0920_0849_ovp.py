# 代码生成时间: 2025-09-20 08:49:26
# Django应用组件 - 用户权限管理系统

# permission_management/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

"""
权限组和权限模型。
"""
class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(Group, related_name='permissions', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def clean(self):
        """
        确保一个Group中不会有重复的Permission。
        """
        group_permissions = Permission.objects.filter(group=self.group)
        if group_permissions.filter(name=self.name).exists() and group_permissions.filter(name=self.name).first() != self:
            raise ValidationError("A permission with this name already exists in this group.")

# permission_management/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Group, Permission

"""
权限管理的视图。
"""
@require_http_methods(['GET', 'POST'])
@login_required
def manage_permissions(request):
    if request.method == 'POST':
        # 这里添加权限管理的POST逻辑
        pass
    else:
        groups = Group.objects.all()
        return render(request, 'permissions/manage_permissions.html', {'groups': groups})

@csrf_exempt
@require_http_methods(['POST'])
def assign_permission(request):
    user_id = request.POST.get('user_id')
    group_id = request.POST.get('group_id')
    # 这里添加分配权限的逻辑
    return JsonResponse({'status': 'success'})

# permission_management/urls.py
from django.urls import path
from . import views

"""
权限管理的URL配置。
"""
urlpatterns = [
    path('manage/', views.manage_permissions, name='manage-permissions'),
    path('assign/', views.assign_permission, name='assign-permission'),
]

# permission_management/admin.py
from django.contrib import admin
from .models import Group, Permission

"""
Django admin界面的配置。
"""
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')
    list_filter = ('group',)
    
# permission_management/tests.py
from django.test import TestCase
from .models import Group, Permission

"""
权限管理系统的测试。
"""
class PermissionManagementTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='Test Group')
        self.permission = Permission.objects.create(name='Test Permission', group=self.group)

    def test_group_creation(self):
        self.assertEqual(self.group.name, 'Test Group')

    def test_permission_creation(self):
        self.assertEqual(self.permission.name, 'Test Permission')
        self.assertEqual(self.permission.group, self.group)

    def test_permission_assignment(self):
        # 这里添加分配权限的测试
        pass