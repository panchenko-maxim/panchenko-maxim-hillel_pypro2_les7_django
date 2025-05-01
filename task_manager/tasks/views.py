from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from tasks.models import Task, Message
from tasks.forms import TaskForm

from tasks.mixins import (OwnerOnlyMixin, SuccessMessageMixin, QueryFilterMixin,
                          TaskCounterMixin, RedirectOnErrorMixin)
from tasks.signals import task_list_view_signal, task_title_requirements_create
from tasks.tasks import send_message

# @login_required
# def tasks_list(request):
#     tasks = Task.objects.filter(user=request.user)
#     return render(request, 'tasks/task_list.html', {'tasks': tasks})

class TaskListView(LoginRequiredMixin, QueryFilterMixin, TaskCounterMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        task_list_view_signal.send(sender=None, request=self.request)
        tasks = super().get_queryset()
        if self.request.user.is_superuser:
            return tasks
        return tasks.filter(user=self.request.user)

# @login_required
# def create_task(request):
#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('task_list')
#     else:
#         form = TaskForm()
#         return render(request, 'tasks/create_task.html', {'form': form})

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, RedirectOnErrorMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task created success!')
    error_redirect_url = reverse_lazy('task_list')

    def form_valid(self, form):
        task_title_requirements_create.send(sender=None, request=self.request, instance=form.instance)
        form.instance.user = self.request.user
        return super().form_valid(form)

# @login_required
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if request.method == "POST":
#         task.delete()
#         return redirect("task_list")
#     return render(request, 'tasks/confirm_delete.html', {'task': task})

class TaskDeleteView(LoginRequiredMixin, OwnerOnlyMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('task_list')
    pk_url_kwarg = 'task_id'
    success_message = _('Deleted success!')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save(update_fields=['completed'], request=request)
    return redirect('task_list')

def create_message(request):
    if request.method == "POST":
        content = request.POST.get('content')
        message = Message.objects.create(content=content)
        send_message.delay(message.id)
        return redirect('message_list')
    return render(request, 'tasks/create_message.html')

def message_list(request):
    messages = Message.objects.all()
    return render(request, 'tasks/message_list.html',
                  {'messages': messages})





