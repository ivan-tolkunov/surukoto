from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import generic
from .models import Todo
from .util import Util
from django.http import HttpResponseRedirect
from django.contrib import messages


util = Util()

class IndexView(generic.ListView):
    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        """Return all the latest todos."""
        return Todo.objects.order_by('-created_at')

def process_voice_command(request):
    audio_file = request.FILES.get('audio_file', None)
    text = util.get_voice_text(audio_file)
    commands = util.get_command(text)
    for command in commands:
        action = command['action']
        if action == "add":
            util.add(command['text'])
        elif action == "complete":
            util.complete(command['task_id'])
        elif action == "delete":
            util.delete(command['task_id'])
        elif action == "error":
            messages.add_message(request, messages.ERROR, command['text'])
        else:
            print("Unknown action")

    return JsonResponse({'success': True})

def update(request, todo_id):
    util.complete(todo_id)
    return redirect('todos:index')