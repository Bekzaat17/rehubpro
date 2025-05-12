from django.contrib import admin
from .models.task_template import TaskTemplate
from .models.assigned_task import AssignedTask

@admin.register(TaskTemplate)
class TaskTemplateAdmin(admin.ModelAdmin):
    # Отображаем в таблице админки задачи: название, тип, дату создания и кто создал
    list_display = ('title', 'task_type', 'created_at', 'created_by')
    # Фильтрация в админке по типу и автору
    list_filter = ('task_type', 'created_by')

@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    # Отображаем прикреплённые задания резидентам
    list_display = ('template', 'resident', 'assigned_by', 'given_date', 'start_date', 'end_date')
    # Фильтрация по полям, связанным с назначением заданий
    list_filter = ('assigned_by', 'given_date', 'start_date', 'end_date')