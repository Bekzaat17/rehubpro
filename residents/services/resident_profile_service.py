from datetime import timedelta
from django.utils import timezone

from residents.models import Resident
from residents.enums import DependencyType
from tasks.models.task_progress import TaskProgress
from roles.models.resident_role_assignment import ResidentRoleAssignment
from residents.serializers.resident_profile_serializer import ResidentProfileSerializer


class ResidentProfileService:

    @staticmethod
    def get_profile_data(resident: Resident) -> dict:
        today = timezone.now().date()
        from_date = today - timedelta(days=14)

        # Основные данные
        base_data = ResidentProfileSerializer(resident).data
        base_data.update({
            "full_name": resident.full_name,
            "birthdate": resident.date_of_birth,
            "dependency_choices": list(DependencyType.choices),
        })

        # Задания за 14 дней
        progress_qs = TaskProgress.objects.filter(
            assigned_task__resident=resident,
            created_at__date__gte=from_date
        ).select_related("assigned_task__task")

        base_data["tasks"] = [
            {
                "date": p.created_at.date(),
                "task_title": p.assigned_task.task.title if p.assigned_task and p.assigned_task.task else "—",
                "status_display": p.get_stage_display(),
                "comment": p.comment or "",
            }
            for p in progress_qs.order_by("created_at")
        ]

        # Роли
        base_data["roles"] = [
            {
                "role_title": r.role.name if r.role else "—",
                "assigned_at": r.assigned_at,
                "unassigned_at": r.unassigned_at,
            }
            for r in ResidentRoleAssignment.objects
            .filter(resident=resident)
            .select_related("role")
            .order_by("-assigned_at")
        ]

        return base_data

    @staticmethod
    def soft_delete(resident: Resident):
        """
        Помечаем как завершившего лечение (soft delete).
        """
        resident.is_active = False
        resident.discharged_at = timezone.now()
        resident.save()