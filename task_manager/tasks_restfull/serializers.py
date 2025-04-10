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

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Name must be include minimum 3 chars')
        return value
