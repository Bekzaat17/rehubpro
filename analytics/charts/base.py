# analytics/charts/base.py

from abc import ABC, abstractmethod

class BaseChartBuilder(ABC):
    @abstractmethod
    def set_data(self, data: dict):
        pass

    @abstractmethod
    def set_title(self, title: str):
        pass

    @abstractmethod
    def build(self) -> dict:
        pass