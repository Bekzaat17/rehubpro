# tasks/views/assign_task_api.py
import json

from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models.task_template import TaskTemplate
from tasks.models.assigned_task import AssignedTask


class AvailableTasksAPI(LoginRequiredMixin, View):
    def get(self, request):
        task_templates = TaskTemplate.objects.all().values("id", "title")
        return JsonResponse({"available_tasks": list(task_templates)})


class AssignTaskAPI(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        resident_id = data["resident_id"]
        task_id = data["task_id"]

        # Создаём назначение (используя шаблон задания)
        AssignedTask.objects.create(
            resident_id=resident_id,
            task_id=task_id,
            assigned_by=request.user,
            status="writing",  # начальный статус
        )

        return JsonResponse({"status": "ok"})

