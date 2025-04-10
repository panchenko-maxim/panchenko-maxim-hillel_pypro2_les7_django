from rest_framework import viewsets
from tasks.models import Task
from tasks_restfull.serializers import TaskSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def perform_create(self, serializer):
        serializer.save()
