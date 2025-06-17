# reports/repositories/report_task_comment_repository.py
from abc import ABC, abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from reports.models import ReportTaskComment, ResidentReport
from tasks.models import AssignedTask # For type hinting

if TYPE_CHECKING:
    from django.db.models import QuerySet

class ReportTaskCommentRepository(AbstractRepository):
    @abstractmethod
    def get_by_report_and_task(self, report: ResidentReport, assigned_task: AssignedTask) -> Optional[ReportTaskComment]:
        pass

    @abstractmethod
    def list_by_report(self, report: ResidentReport) -> Sequence[ReportTaskComment]:
        pass

    @abstractmethod
    def update_or_create(self, report: ResidentReport, assigned_task: AssignedTask, defaults: Optional[dict] = None) -> tuple[ReportTaskComment, bool]:
        pass

    @abstractmethod
    def delete_for_report_and_task(self, report: ResidentReport, assigned_task: AssignedTask) -> None:
        pass


class DjangoReportTaskCommentRepository(ReportTaskCommentRepository):
    def get_by_report_and_task(self, report: ResidentReport, assigned_task: AssignedTask) -> Optional[ReportTaskComment]:
        try:
            return ReportTaskComment.objects.get(report=report, assigned_task=assigned_task)
        except ReportTaskComment.DoesNotExist:
            return None

    def list_by_report(self, report: ResidentReport) -> 'QuerySet[ReportTaskComment]':
        return ReportTaskComment.objects.filter(report=report).select_related('assigned_task', 'assigned_task__task')

    def update_or_create(self, report: ResidentReport, assigned_task: AssignedTask, defaults: Optional[dict] = None) -> tuple[ReportTaskComment, bool]:
        return ReportTaskComment.objects.update_or_create(
            report=report,
            assigned_task=assigned_task,
            defaults=defaults or {}
        )

    def delete_for_report_and_task(self, report: ResidentReport, assigned_task: AssignedTask) -> None:
        ReportTaskComment.objects.filter(report=report, assigned_task=assigned_task).delete()
