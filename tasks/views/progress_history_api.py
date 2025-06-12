# tasks/views/progress_history_api.py

from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from residents.models import Resident
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_progress import TaskProgress
import json


class ProgressHistoryAPI(LoginRequiredMixin, View):
    def get(self, request, resident_id):
        tasks = AssignedTask.objects.filter(resident_id=resident_id).order_by("-assigned_at")
        result = []

        for task in tasks:
            progresses = TaskProgress.objects.filter(assigned_task=task).order_by("-created_at")
            result.append({
                "task": {
                    "id": task.id,
                    "title": task.task.title,
                    "assigned_at": task.assigned_at.strftime("%Y-%m-%d %H:%M"),
                },
                "progresses": [
                    {
                        "id": progress.id,
                        "stage": progress.stage,
                        "comment": progress.comment,
                        "created_at": progress.created_at.strftime("%Y-%m-%d %H:%M")
                    }
                    for progress in progresses
                ]
            })

        return JsonResponse(result, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 2})



class AddTaskProgressAPI(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        task = AssignedTask.objects.get(id=data["task_id"])
        # только добавление, без изменения/удаления
        TaskProgress.objects.create(
            assigned_task=task,
            stage=data["stage"],
            comment=data.get("comment", ""),
            updated_by=request.user
        )
        # также обнови статус задачи, если нужно
        task.status = data["stage"]  # либо map
        task.save(update_fields=["status"])
        return JsonResponse({"status": "ok"})