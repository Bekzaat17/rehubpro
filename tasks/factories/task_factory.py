from tasks.enums import TaskType
from residents.models import Resident
from tasks.logic.short_term_task import ShortTermTask
from tasks.logic.long_term_task import LongTermTask
from tasks.logic.test_task import TestTask
from tasks.logic.base_task import BaseTask


class TaskFactory:
    """
    Абстрактная фабрика, создающая нужный тип задания.
    По принципу Open/Closed: легко расширяется без изменения кода.
    """

    @staticmethod
    def get_task(task_type: TaskType, resident: Resident, title: str, comment: str = "") -> BaseTask:
        if task_type == TaskType.SHORT_TERM:
            return ShortTermTask(resident, title, comment)
        elif task_type == TaskType.LONG_TERM:
            return LongTermTask(resident, title, comment)
        elif task_type == TaskType.TEST:
            return TestTask(resident, title, comment)
        else:
            raise ValueError(f"Неизвестный тип задания: {task_type}")