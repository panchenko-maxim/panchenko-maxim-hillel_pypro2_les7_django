from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks_restfull.views import TaskModelViewSet


router = DefaultRouter()
router.register(r'tasks', TaskModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]