# analytics/metrics/base.py

from abc import ABC, abstractmethod
from typing import Type
from analytics.charts.base import BaseChartBuilder


class BaseMetric(ABC):
    def __init__(self, queryset):
        self.queryset = queryset

    @abstractmethod
    def calculate(self):
        pass

    def get_chart_builder_class(self) -> Type[BaseChartBuilder]:
        from analytics.charts.line_chart import LineChartBuilder
        return LineChartBuilder