#tasks/strategy/short_term_task.py
from .base_task import BaseTask
from tasks.models.assigned_task import AssignedTask


class ShortTermTask(BaseTask):
    """
    Краткосрочное задание.
    """

    def create(self) -> AssignedTask:
        return AssignedTask.objects.create(
            resident=self.resident,
            task=self.template,
            assigned_by=None,
        )