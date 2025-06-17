# reports/repositories/__init__.py
from .resident_report_repository import ResidentReportRepository, DjangoResidentReportRepository
from .report_task_comment_repository import ReportTaskCommentRepository, DjangoReportTaskCommentRepository
from .resident_report_role_status_repository import ResidentReportRoleStatusRepository, DjangoResidentReportRoleStatusRepository

__all__ = [
    "ResidentReportRepository", "DjangoResidentReportRepository",
    "ReportTaskCommentRepository", "DjangoReportTaskCommentRepository",
    "ResidentReportRoleStatusRepository", "DjangoResidentReportRoleStatusRepository",
]
