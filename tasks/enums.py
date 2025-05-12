# tasks/enums.py

from enum import Enum

class TaskType(Enum):
    TEST = 'test'
    SHORT_TERM = 'short_term'
    LONG_TERM = 'long_term'

    def __str__(self):
        return self.value