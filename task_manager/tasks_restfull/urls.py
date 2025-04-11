from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks_restfull.views import TaskModelViewSet, TaskReadOnlyViewSet


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)
router.register(r'tasks-readonly', TaskReadOnlyViewSet, basename='tasks-readonly')

urlpatterns = [
    path('', include(router.urls)),
]