# reports/repositories/resident_report_repository.py
from abc import ABC, abstractmethod
from typing import Optional, Sequence, TYPE_CHECKING
from datetime import date

from django.db.models import QuerySet

from core.patterns.repository import AbstractRepository
from reports.models import ResidentReport
from residents.models import Resident # For type hinting if needed for resident_id

if TYPE_CHECKING:
    from django.db.models import QuerySet


class ResidentReportRepository(AbstractRepository):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[ResidentReport]:
        pass

    @abstractmethod
    def get_by_resident_and_date(self, resident: Resident, report_date: date) -> Optional[ResidentReport]:
        pass

    @abstractmethod
    def list_by_resident(self, resident: Resident) -> Sequence[ResidentReport]:
        pass

    @abstractmethod
    def add(self, report: ResidentReport) -> ResidentReport:
        pass

    @abstractmethod
    def update(self, report: ResidentReport) -> ResidentReport:
        pass

    @abstractmethod
    def delete(self, report: ResidentReport) -> None:
        pass

    @abstractmethod
    def get_or_create(self, resident: Resident, report_date: date, defaults: Optional[dict] = None) -> tuple[ResidentReport, bool]:
        pass


class DjangoResidentReportRepository(ResidentReportRepository):
    def get_by_id(self, id: int) -> Optional[ResidentReport]:
        try:
            return ResidentReport.objects.select_related(
                'resident', 'created_by', 'emotional_state', 'physical_state',
                'motivation', 'daily_dynamics', 'mrp_activity', 'family_activity'
            ).prefetch_related(
                'positive_traits', 'negative_traits', 'task_comments', 'role_statuses'
            ).get(id=id)
        except ResidentReport.DoesNotExist:
            return None

    def get_by_resident_and_date(self, resident: Resident, report_date: date) -> Optional[ResidentReport]:
        try:
            return ResidentReport.objects.select_related(
                'resident', 'created_by', 'emotional_state', 'physical_state',
                'motivation', 'daily_dynamics', 'mrp_activity', 'family_activity'
            ).prefetch_related(
                'positive_traits', 'negative_traits', 'task_comments', 'role_statuses'
            ).get(resident=resident, date=report_date)
        except ResidentReport.DoesNotExist:
            return None

    def list_by_resident(self, resident: Resident) -> 'QuerySet[ResidentReport]':
        return ResidentReport.objects.filter(resident=resident).order_by('-date')

    def add(self, report: ResidentReport) -> ResidentReport:
        # Assumes all related objects (FKs, M2M) are already handled or set on the instance
        report.save()
        return report

    def update(self, report: ResidentReport) -> ResidentReport:
        # Assumes all related objects (FKs, M2M) are already handled or set on the instance
        report.save()
        return report

    def delete(self, report: ResidentReport) -> None:
        report.delete()

    def get_or_create(self, resident: Resident, report_date: date, defaults: Optional[dict] = None) -> tuple[ResidentReport, bool]:
        # This directly uses the ORM's get_or_create, which is often what's needed.
        # The factory can use this.
        return ResidentReport.objects.get_or_create(resident=resident, date=report_date, defaults=defaults or {})
