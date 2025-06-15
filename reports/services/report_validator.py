from django.utils.timezone import localdate
from django.core.exceptions import ValidationError
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_progress import TaskProgress
from roles.models.resident_role_assignment import ResidentRoleAssignment
from reports.models.resident_report import ResidentReport


class ReportValidator:
    """
    Валидатор отчёта:
    - До создания: проверка комментариев по задачам и ролям
    - После создания: проверка обязательных полей и характеристик
    """

    def __init__(self, resident, date=None):
        self.resident = resident
        self.date = date or localdate()
        self.task_comments = {}
        self.role_statuses = {}

    def set_task_comments(self, task_comments: dict):
        self.task_comments = task_comments

    def set_role_statuses(self, role_statuses: dict):
        self.role_statuses = role_statuses

    def validate_pre_creation(self):
        """
        Проверка до создания отчёта:
        - Активные задания должны иметь комментарии
        - Активные роли должны иметь статус
        """
        # TODO: task comments validate by todays date, do not validate role statuses
        self._validate_task_comments()
        self._validate_role_statuses()

    def validate_post_creation(self, report: ResidentReport):
        """
        Проверка после создания отчёта:
        - Обязательные поля (эмоции, физика, мотивация и т.д.)
        - Характеристики
        - Проверка заполнения блока УСТС
        """
        self._validate_required_fields(report)
        self._validate_traits(report)
        self._validate_usts(report)

    def _validate_task_comments(self):
        active_tasks = AssignedTask.objects.filter(
            resident=self.resident,
            status__in=[AssignedTask.Status.WRITING, AssignedTask.Status.SUBMITTING]
        )

        missing = []
        for task in active_tasks:
            if task.id not in self.task_comments or not self.task_comments[task.id].strip():
                missing.append(str(task))

        if missing:
            raise ValidationError(f"Не указаны комментарии по заданиям: {', '.join(missing)}")

    def _validate_role_statuses(self):
        active_roles = ResidentRoleAssignment.objects.filter(
            resident=self.resident,
            assigned_at__lte=self.date
        ).filter(
            unassigned_at__isnull=True
        ) | ResidentRoleAssignment.objects.filter(
            resident=self.resident,
            assigned_at__lte=self.date,
            unassigned_at__gte=self.date
        )

        missing = []
        for role in active_roles:
            if str(role.id) not in self.role_statuses or not self.role_statuses[str(role.id)]:
                missing.append(str(role))

        if missing:
            raise ValidationError(f"Не указана ответственность по ролям: {', '.join(missing)}")

    def _validate_required_fields(self, report: ResidentReport):
        missing = []

        if not report.emotional_state:
            missing.append("Эмоциональное состояние")
        if not report.physical_state:
            missing.append("Физическое состояние")
        if not report.motivation:
            missing.append("Мотивация")
        if not report.daily_dynamics:
            missing.append("Динамика")
        if not report.mrp_activity:
            missing.append("Участие в МРП")
        if not report.family_activity:
            missing.append("Семейное взаимодействие")
        if not report.comment or report.comment.strip() == "":
            missing.append("Комментарий")

        if missing:
            raise ValidationError(f"Не заполнены обязательные поля: {', '.join(missing)}")

    def _validate_traits(self, report: ResidentReport):
        if not report.positive_traits.exists() and not report.negative_traits.exists():
            raise ValidationError("Не выбраны характеристики (достоинства или дефекты)")

    def _validate_usts(self, report: ResidentReport):
        """
        Проверка заполнения блока УСТС:
        - Должно быть указано, обозначил ли УСТС (ровно/не ровно)
        - Должно быть указано, имеет ли формат
        """
        if report.usts_info_shared is None:
            raise ValidationError("Не указано: Информацию подает (ровно / не ровно)")

        if report.usts_format_followed is None:
            raise ValidationError("Не указано: Имеет ли формат УСТС")
        # (опционально) требовать комментарий, если хоть одно "нет"
        # if not report.usts_info_shared or not report.usts_format_followed:
        #     if not report.usts_comment or report.usts_comment.strip() == "":
        #         raise ValidationError("При нарушении УТС необходимо указать комментарий")