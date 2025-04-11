from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from yaml import serialize

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


class TaskReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["completed", "user"]


class TaskCustomViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Task.objects.filter(completed=False)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        pass