from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
                'id', 'title', 'description', 'completed',
                'created_at', 'updated_at', 'user', 'moderation_status'
        ]
        read_only_fields = ['created_at', 'updated_at']