from django.shortcuts import render
from django.urls import path
from permissions.views import list_users, manage_permissions


urlpatterns = [
    path('user-list/', list_users, name='user_list'),
    path('manage-permissions/<int:user_id>', manage_permissions, name='manage_permissions'),
    path('/', lambda request: render(request, 'home.html'), name='user_permissions'),
]