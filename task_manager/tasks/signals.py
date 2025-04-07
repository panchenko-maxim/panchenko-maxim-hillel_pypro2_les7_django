from django.core.exceptions import PermissionDenied
from django.template.context_processors import request

from tasks.models import Task, TaskLog
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib import messages

@receiver(post_save, sender=Task)
def notify_task_completed(sender, instance, created, update_fields, **kwargs):
    request = kwargs.get('request')
    if request and not created and update_fields and 'completed' in update_fields and instance.complited:
        messages.success(request, f'Task "{instance.title}" successfully completed')

@receiver(pre_delete, sender=Task)
def notify_task_deleted(sender, instance, **kwargs):
    TaskLog.objects.create(action=TaskLog.DELETE, user=instance.user)
    # breakpoint()

@receiver(pre_delete, sender=Task)
def notify_task_deleted_restricted(sender, instance, **kwargs):
    if not instance.completed:
        raise Task.DoesNotExist
    TaskLog.objects.create(action=TaskLog.DELETE, user=instance.user)