# reports/repositories/resident_report_role_status_repository.py
from abc import ABC, abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from reports.models import ResidentReportRoleStatus, ResidentReport
from roles.models import ResidentRoleAssignment # For type hinting

if TYPE_CHECKING:
    from django.db.models import QuerySet

class ResidentReportRoleStatusRepository(AbstractRepository):
    @abstractmethod
    def get_by_report_and_assignment(self, report: ResidentReport, assignment: ResidentRoleAssignment) -> Optional[ResidentReportRoleStatus]:
        pass

    @abstractmethod
    def list_by_report(self, report: ResidentReport) -> Sequence[ResidentReportRoleStatus]:
        pass

    @abstractmethod
    def update_or_create(self, report: ResidentReport, assignment: ResidentRoleAssignment, defaults: Optional[dict] = None) -> tuple[ResidentReportRoleStatus, bool]:
        pass


class DjangoResidentReportRoleStatusRepository(ResidentReportRoleStatusRepository):
    def get_by_report_and_assignment(self, report: ResidentReport, assignment: ResidentRoleAssignment) -> Optional[ResidentReportRoleStatus]:
        try:
            return ResidentReportRoleStatus.objects.get(report=report, role_assignment=assignment)
        except ResidentReportRoleStatus.DoesNotExist:
            return None

    def list_by_report(self, report: ResidentReport) -> 'QuerySet[ResidentReportRoleStatus]':
        return ResidentReportRoleStatus.objects.filter(report=report).select_related('role_assignment', 'role_assignment__role')

    def update_or_create(self, report: ResidentReport, assignment: ResidentRoleAssignment, defaults: Optional[dict] = None) -> tuple[ResidentReportRoleStatus, bool]:
        return ResidentReportRoleStatus.objects.update_or_create(
            report=report,
            role_assignment=assignment,
            defaults=defaults or {}
        )
