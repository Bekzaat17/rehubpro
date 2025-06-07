#tasks/strategy/task_factory.py
from typing import Type
from tasks.enums.task_type import TaskType
from .base_task import BaseTask
from .short_term_task import ShortTermTask
from .long_term_task import LongTermTask
from .test_task import TestTask
from residents.models import Resident
from tasks.models.task_template import TaskTemplate


class TaskFactory:
    """
    Абстрактная фабрика для создания задания нужного типа.
    """

    task_map: dict[str, Type[BaseTask]] = {
        TaskType.SHORT_TERM: ShortTermTask,
        TaskType.LONG_TERM: LongTermTask,
        TaskType.TEST: TestTask,
    }

    @classmethod
    def get_task(cls, task_type: str, resident: Resident, template: TaskTemplate, comment: str = "") -> BaseTask:
        if task_type not in cls.task_map:
            raise ValueError(f"Task type '{task_type}' not supported.")
        task_class = cls.task_map[task_type]
        return task_class(resident=resident, template=template, comment=comment)