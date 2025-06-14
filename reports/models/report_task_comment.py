from django.db import models

from reports.models.resident_report import ResidentReport
from tasks.models.assigned_task import AssignedTask


class ReportTaskComment(models.Model):
    """
    Комментарии к активным задачам резидента в рамках ежедневного отчёта.
    Обязательны для заполнения отчёта.
    """

    report = models.ForeignKey(
        ResidentReport,
        on_delete=models.CASCADE,
        related_name="task_comments"
    )
    assigned_task = models.ForeignKey(
        AssignedTask,
        on_delete=models.CASCADE,
        related_name="report_comments",
        help_text="Активная задача резидента на момент отчёта"
    )
    comment = models.TextField()

    class Meta:
        unique_together = ("report", "assigned_task")
        verbose_name = "Комментарий к задаче"
        verbose_name_plural = "Комментарии к задачам"

    def __str__(self):
        return f"Задача {self.assigned_task.id} | {self.report.resident} — {self.report.date}"