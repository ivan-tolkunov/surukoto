from django.urls import path
from . import views

app_name='todos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:todo_id>/delete', views.delete, name='delete'),
    path('<int:todo_id>/update', views.update, name='update'),
    path('process-voice-command/', views.process_voice_command, name='process_voice_command'),
    path('add/', views.add, name='add')
]