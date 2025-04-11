from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from tasks.models import Task
from tasks_restfull.serializers import TaskSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['completed', 'user']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'completed']
    
    def perform_create(self, serializer):
        serializer.save()
