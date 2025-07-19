from django.db import transaction
from django.utils.timezone import localdate
from django.core.exceptions import ValidationError

from reports.models.resident_report import ResidentReport
from reports.models.resident_report_role_status import ResidentReportRoleStatus
from reports.models.report_task_comment import ReportTaskComment
from roles.models.resident_role_assignment import ResidentRoleAssignment
from tasks.models.assigned_task import AssignedTask
from reports.services.report_validator import ReportValidator


class ReportFactory:
    """
    Фабрика для создания или обновления полного отчёта по резиденту.
    """

    def __init__(self, resident, created_by, date=None, skip_validation=False):
        self.resident = resident
        self.created_by = created_by
        self.date = date or localdate()
        self.skip_validation = skip_validation

    @transaction.atomic
    def create_or_update_report(self, data, task_comments, role_statuses):
        """
        Создаёт или обновляет отчёт и все связанные сущности.

        :param data: словарь с полями отчёта (emotional_state, motivation и т.п.)
        :param task_comments: словарь {assigned_task_id: comment}
        :param role_statuses: словарь {resident_role_assignment_id: "responsible"/"irresponsible"}
        :return: объект ResidentReport
        """

        # 1. Валидируем ДО создания/обновления ResidentReport
        validator = ReportValidator(self.resident, self.date, skip_validation=self.skip_validation)
        validator.set_task_comments(task_comments)
        validator.set_role_statuses(role_statuses)
        validator.validate_pre_creation()

        # 2. Создаём или обновляем основной отчёт
        report, created = ResidentReport.objects.update_or_create(
            resident=self.resident,
            date=self.date,
            defaults={
                "created_by": self.created_by,
                "emotional_state": data.get("emotional_state"),
                "physical_state": data.get("physical_state"),
                "motivation": data.get("motivation"),
                "daily_dynamics": data.get("daily_dynamics"),
                "mrp_activity": data.get("mrp_activity"),
                "family_activity": data.get("family_activity"),
                "comment": data.get("comment", "").strip(),
                "usts_info_shared": data.get("usts_info_shared"),
                "usts_format_followed": data.get("usts_format_followed"),
                "usts_comment": data.get("usts_comment", "").strip(),
            }
        )

        # 3. ManyToMany поля (характер)
        if "positive_traits" in data:
            report.positive_traits.set(data["positive_traits"])
        if "negative_traits" in data:
            report.negative_traits.set(data["negative_traits"])

        # 4. Комментарии по заданиям (обновляем или создаём, не удаляя)
        for task_id, comment in task_comments.items():
            task = AssignedTask.objects.get(id=task_id)
            ReportTaskComment.objects.update_or_create(
                report=report,
                assigned_task=task,
                defaults={"comment": comment.strip()}
            )

        # 5. Ответственность по ролям (обновляем или создаём, не удаляя)
        for assignment_id, status in role_statuses.items():
            role_assignment = ResidentRoleAssignment.objects.get(id=assignment_id)
            ResidentReportRoleStatus.objects.update_or_create(
                report=report,
                role_assignment=role_assignment,
                defaults={"status": status}
            )

        # 6. Валидируем ПОСЛЕ создания/обновления отчёта
        validator.validate_post_creation(report)

        return report