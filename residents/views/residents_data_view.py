from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.utils.timezone import now

from residents.models import Resident
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_progress import TaskProgress
from roles.models.resident_role_assignment import ResidentRoleAssignment
from core.util import format_date


class ResidentsDataView(LoginRequiredMixin, View):
    """
    API-представление, возвращающее список резидентов в виде JSON
    для таблицы в кабинете консультанта.
    """

    def get(self, request):
        residents = Resident.objects.filter(is_active=True).order_by("last_name")

        column_names = [
            "ФИО",
            "Статус",
            "Дата поступления",
            "Текущее задание",
            "Последний прогресс",
            "Активные роли",
            "Заметки",
            "Тип зависимости"
        ]

        rows = []
        today = now().date()

        for r in residents:
            full_name = f"{r.last_name} {r.first_name} {r.middle_name or ''}".strip()

            # Текущее задание
            current_task = AssignedTask.objects.select_related("task").filter(
                resident=r,
                status__in=["writing", "submitting"]
            ).order_by("-assigned_at").first()

            if current_task:
                task_title = current_task.task.title
                task_date = format_date(current_task.assigned_at)
                task_display = f"{task_title}<br><small>Назначено: {task_date}</small>"
            else:
                task_display = "—"

            # Последний прогресс
            last_progress = TaskProgress.objects.filter(
                assigned_task__resident=r,
                stage__in=["writing", "submitting"]
            ).order_by("-created_at").first()

            if last_progress:
                stage_display = last_progress.get_stage_display()
                comment = last_progress.comment.strip()
                if comment:
                    progress_display = f"{stage_display}: {comment}"
                else:
                    progress_display = stage_display
            else:
                progress_display = "—"

            # Активные роли
            roles = ResidentRoleAssignment.objects.filter(
                resident=r,
                assigned_at__lte=today
            ).filter(
                unassigned_at__isnull=True
            ) | ResidentRoleAssignment.objects.filter(
                resident=r,
                assigned_at__lte=today,
                unassigned_at__gte=today
            )

            if roles.exists():
                roles_display = "; ".join(f"{role.role.name} ({format_date(role.assigned_at)})" for role in roles)
            else:
                roles_display = "—"

            # Заметки
            notes = r.notes.strip() if r.notes else "—"

            # Тип зависимости
            dep_type = r.get_dependency_type_display() if r.dependency_type else "—"

            # Добавляем ID + данные
            rows.append({
                "id": r.id,
                "cells": [
                    full_name,
                    r.get_status_display(),
                    format_date(r.date_of_admission),
                    task_display,
                    progress_display,
                    roles_display,
                    notes,
                    dep_type
                ]
            })

        return JsonResponse({
            "columns": column_names,
            "rows": rows
        })