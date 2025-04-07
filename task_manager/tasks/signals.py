from django.template.context_processors import request

from tasks.models import Task
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib import messages

@receiver(post_save, sender=Task)
def notify_task_completed(sender, instance, created, updated, update_fields, **kwargs):
    request = kwargs.get('request')
    if request and not created and update_fields and 'completed' in update_fields and instance.complited:
        messages.success(request, f'Task "{instance.title}" successfully completed')