# tasks/urls.py
from django.urls import path
from .views.templates.task_templates_view import TaskTemplatesView, TaskTemplateAPI


app_name = 'tasks'

urlpatterns = [
    path('templates/', TaskTemplatesView.as_view(), name='task_templates'),
    path('templates/api/', TaskTemplateAPI.as_view(), name='task_templates_api'),]