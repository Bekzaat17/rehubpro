from datetime import date
from tasks.logic.base_task import BaseTask
from tasks.enums import TaskType
from tasks.models.assigned_task import AssignedTask


class TestTask(BaseTask):
    """
    Тестовое задание — может не требовать end_date.
    """

    def create(self) -> AssignedTask:
        today = date.today()
        return AssignedTask.objects.create(
            resident=self.resident,
            task_title=self.title,
            task_type=TaskType.TEST.value,
            comment=self.comment,
            given_date=today,
            start_date=None,
            end_date=None,
        )