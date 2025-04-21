from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('<int:task_id>/complete/', views.complete_task, name='task_complete'),
    path('messages/', views.message_list, name='message_list'),
    path('create_message/', views.create_message, name='create_message'),
]