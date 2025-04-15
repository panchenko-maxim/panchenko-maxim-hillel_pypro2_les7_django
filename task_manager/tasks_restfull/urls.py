from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks_restfull.views import (TaskModelViewSet, TaskReadOnlyViewSet,
                                  TaskCustomViewSet, TaskFilterViewSet, TaskCreateViewSet,
                                  TaskUpdateViewSet, CustomAuthToken, login, login_jwt)


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)
router.register(r'tasks-readonly', TaskReadOnlyViewSet, basename='tasks-readonly')
router.register(r'tasks-unfinished', TaskCustomViewSet, basename='tasks-unfinished')
router.register(r'tasks-filtered', TaskFilterViewSet, basename='tasks-filtered')
router.register(r'task-create', TaskCreateViewSet, basename='task-create')
router.register(r'task-update', TaskUpdateViewSet, basename='task-update')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login, name="login"),
    path('login-jwt/', login_jwt, name="login-jwt"),
]