from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from tasks.models import Task
from tasks.forms import TaskForm


# @login_required
# def tasks_list(request):
#     tasks = Task.objects.filter(user=request.user)
#     return render(request, 'tasks/task_list.html', {'tasks': tasks})

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = super().get_queryset()
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

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# @login_required
# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if request.method == "POST":
#         task.delete()
#         return redirect("task_list")
#     return render(request, 'tasks/confirm_delete.html', {'task': task})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('task_list')
    pk_url_kwarg = 'task_id'






