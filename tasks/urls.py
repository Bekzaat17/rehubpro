# tasks/urls.py
from django.urls import path
from .views.templates.task_templates_view import TaskTemplatesView, TaskTemplateAPI
from .views.resident_tasks_view import ResidentTasksView
from tasks.views.progress_history_api import AddTaskProgressAPI, ProgressHistoryAPI
from .views.assign_task_api import AvailableTasksAPI, AssignTaskAPI


app_name = 'tasks'

urlpatterns = [
    path('templates/', TaskTemplatesView.as_view(), name='task_templates'),
    path('templates/api/', TaskTemplateAPI.as_view(), name='task_templates_api'),
    path('templates/api/<int:template_id>/', TaskTemplateAPI.as_view(), name='template_api_delete'),
    path('resident-tasks/', ResidentTasksView.as_view(), name='resident_tasks'),
    path("add-progress/", AddTaskProgressAPI.as_view(), name="add_progress_api"),
    path('available/', AvailableTasksAPI.as_view(), name='available_tasks_api'),
    path('assign/', AssignTaskAPI.as_view(), name='assign_task_api'),
    path("progress-history/resident/<int:resident_id>/", ProgressHistoryAPI.as_view(), name="progress-history"),

]