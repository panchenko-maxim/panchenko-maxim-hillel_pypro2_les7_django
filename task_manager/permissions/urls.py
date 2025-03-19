from django.urls import path
from permissions.views import list_users, manage_permissions, tags_page


urlpatterns = [
    path('list_users/', list_users, name='list_users'),
    path('manage-permissions/<int:user_id>', manage_permissions, name='manage_permissions'),
    path('tags/', tags_page, name='tags'),
]