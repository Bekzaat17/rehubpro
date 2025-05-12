from abc import ABC, abstractmethod
from datetime import date
from residents.models import Resident
from tasks.models.assigned_task import AssignedTask
from tasks.enums import TaskType


class BaseTask(ABC):
    """
    Абстрактный базовый класс задания.
    По SOLID: реализует принцип единственной ответственности (Single Responsibility).
    """

    def __init__(self, resident: Resident, title: str, comment: str = ""):
        self.resident = resident
        self.title = title
        self.comment = comment

    @abstractmethod
    def create(self) -> AssignedTask:
        """
        Метод, который должен реализовать каждый подкласс.
        """
        pass