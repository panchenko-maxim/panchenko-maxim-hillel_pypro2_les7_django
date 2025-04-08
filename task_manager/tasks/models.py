from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    MODERATION_STEP = 1
    APPROVED = 0

    STATUS_CHOICES = [
        (MODERATION_STEP, 'On moderation'),
        (APPROVED, 'Approved')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    moderation_status = models.IntegerField(choices=STATUS_CHOICES, default=MODERATION_STEP)

    def __str__(self):
        return self.title

class TaskLog(models.Model):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
    STATUS_CHANGED = 4
    TASK_LIST_VIEWED = 5

    ACTION_CHOICES = [
        (CREATE, 'Task created'),
        (UPDATE, 'Task completed'),
        (DELETE, 'Task deleted'),
        (STATUS_CHANGED, 'Status changed'),
        (TASK_LIST_VIEWED, 'User looked at task list page'),
    ]

    action_date = models.DateTimeField(auto_now_add=True)
    action = models.IntegerField(choices=ACTION_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_status = models.IntegerField(blank=True, null=True, default=Task.MODERATION_STEP)
