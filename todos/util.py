
from django.core.files.storage import default_storage
from todos.models import Todo
import whisper
import requests
import json
import os

OPENROUTER_KEY = os.environ['OPENROUTER_KEY']

class Util:
    def __init__(self, model="base", prompt = ( "As an advanced TODO app manager, your role is to process user instructions "
                                                "and respond exclusively in a JSON-formatted array containing objects. These objects "
                                                "represent four possible actions: 'add (to add new task)', 'complete'(to complete task), 'delete'(to delete task), and 'error' (for unclear instructions). "
                                                "Your responses should clearly indicate the relevant action. For instance, if a user says, 'I want to visit my grandma.', "
                                                "your reply should be: {'action': 'add', 'text': 'Visit grandma'}. "
                                                "For delete and complete also add the 'task_id' field."
                                                "The TODOs are structured as follows: \n")
                                        ):
        self.model = whisper.load_model(model)
        self.prompt = prompt

        
    def get_voice_text(self, voice):
        file_name = default_storage.save(voice.name, voice)
        audio = whisper.load_audio("media/" +file_name)
        audio = whisper.pad_or_trim(audio)
        result = self.model.transcribe("media/" + file_name)
        default_storage.delete(file_name)
        return result["text"].strip()
    
    def get_command(self, text):
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers= {
                "Authorization" : f"Bearer {OPENROUTER_KEY}"
            },
            data=json.dumps({
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": f"{ text } { self.todo_to_string() }"},
                ]
            })
        )

        print(self.todo_to_string())
        return json.loads(response.json()["choices"][0]["message"]["content"])
    
    def add(self, text):
        Todo.objects.create(title=text)
    
    def complete(self, id):
        todo = Todo.objects.get(pk=id)
        if todo.isCompleted:
            todo.isCompleted = False
        else: 
            todo.isCompleted = True
            
        todo.save()
    
    def delete(self, id):
        todo = Todo.objects.get(pk=id)
        todo.delete()

    def todo_to_string(self):
        str = ""
        for todo in Todo.objects.all():
            str += f"id: {todo.id}, text: {todo.title}, completed: {todo.isCompleted} \n"

        return str