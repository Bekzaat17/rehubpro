# analytics/metrics/base.py

from abc import ABC, abstractmethod
from typing import Type
from analytics.charts.base import BaseChartBuilder
from reports.models import ResidentReport


class BaseMetric(ABC):
    def __init__(self, queryset):
        self.queryset = queryset

    @abstractmethod
    def calculate(self):
        pass

    def get_chart_builder_class(self) -> Type[BaseChartBuilder]:
        from analytics.charts.line_chart import LineChartBuilder
        return LineChartBuilder

    @classmethod
    def get_base_queryset(cls, filters):
        return ResidentReport.objects.all()

    @classmethod
    def get_filter_field(cls):
        return "date"  # По умолчанию — для ResidentReport