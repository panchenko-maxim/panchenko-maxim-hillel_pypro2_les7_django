from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]