from datetime import date
from tasks.logic.base_task import BaseTask
from tasks.enums import TaskType
from tasks.models.assigned_task import AssignedTask


class ShortTermTask(BaseTask):
    """
    Краткосрочное задание, выполняемое за 1 день.
    """

    def create(self) -> AssignedTask:
        today = date.today()
        return AssignedTask.objects.create(
            resident=self.resident,
            task_title=self.title,
            task_type=TaskType.SHORT_TERM.value,
            comment=self.comment,
            given_date=today,
            start_date=today,
            end_date=today,
        )