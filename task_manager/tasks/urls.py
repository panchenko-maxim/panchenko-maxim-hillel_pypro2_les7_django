from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.tasks_list, name='task_list'),
    path('create/', views.create_task, name='task_create'),
    path('<int:task_id>/delete/', views.delete_task, name='task_delete'),
]