from django.contrib import admin
from tasks.models import Task, TaskLog, Message

admin.site.register(Task)
admin.site.register(TaskLog)
admin.site.register(Message)


    
