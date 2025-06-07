#tasks/strategy/base_task.py
from abc import ABC, abstractmethod
from residents.models import Resident
from tasks.models.assigned_task import AssignedTask
from tasks.models.task_template import TaskTemplate


class BaseTask(ABC):
    """
    Абстрактный базовый класс задания.
    """

    def __init__(self, resident: Resident, template: TaskTemplate, comment: str = ""):
        self.resident = resident
        self.template = template
        self.comment = comment

    @abstractmethod
    def create(self) -> AssignedTask:
        """
        Метод должен создавать назначенное задание.
        """
        pass