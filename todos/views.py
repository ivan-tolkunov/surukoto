from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from .util import Util
from django.http import HttpResponseRedirect

util = Util()

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by('-created_at')

def add(request):
    title = request.POST['title']
    Todo.objects.create(title=title)

    return redirect('todos:index')

def process_voice_command(request):
    audio_file = request.FILES.get('audio_file', None)
    text = util.get_voice_text(audio_file)
    commands = util.get_command(text)
    print(text)
    for command in commands:
        match command['action']:
            case "add":
                util.add(command['text'])
                print("Added: " + command['text'])
            case "complete":
                util.complete(command['task_id'])
            case "delete":
                util.delete(command['task_id'])
            case "error":
                print("error")

    return redirect('todos:index')

def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('todos:index')

def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    isCompleted = request.POST.get('isCompleted', False)
    if isCompleted == 'on':
        isCompleted = True
    
    todo.isCompleted = isCompleted

    todo.save()
    return redirect('todos:index')