
from tasks.models import Task, TaskLog
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver, Signal
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

@receiver([pre_save, post_save], sender=Task)
def moderate_tasks(sender, instance, created=False, update_fields=None,**kwargs):
    if kwargs.get('signal') == pre_save:
        if (instance.moderation_status == Task.APPROVED) and not instance.user.is_superuser:
            instance.moderation_status = Task.MODERATION_STEP
        elif instance.pk:
            old_task = Task.objects.get(id=instance.pk)
            if old_task.moderation_status != instance.moderation_status:
                TaskLog.objects.create(
                    action=TaskLog.STATUS_CHANGED,
                    user=instance.user,
                    task_status=instance.moderation_status
                )
        else:
            instance.status = Task.MODERATION_STEP
    elif kwargs.get('signal') == post_save:
        if (instance.moderation_status == Task.APPROVED) and instance.user.is_superuser:
            TaskLog.objects.create(
                action=TaskLog.STATUS_CHANGED,
                user=instance.user,
                task_status=instance.moderation_status
            )

task_list_view_signal = Signal()

@receiver(task_list_view_signal)
def log_task_list_view(sender, request, **kwargs):
    if request:
        TaskLog.objects.create(
            action=TaskLog.TASK_LIST_VIEWED,
            user=request.user
        )
        # messages.success(request, f'User {request.user} viewed the task list page')

task_title_requirements_create = Signal()

@receiver(task_title_requirements_create)
def notify_requirements(sender, request, instance, **kwargs):
    if request and instance:
        if len(instance.title) == 0:
            instance.title = "Default title"
            instance.user = request.user
            instance.save()
        if len(instance.title) < 3:
            messages.warning(request, f'Its ok, but we recommend the longer title, at least 3 chars')
