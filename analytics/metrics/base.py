# analytics/metrics/base.py

from abc import ABC, abstractmethod

class BaseMetric(ABC):
    def __init__(self, queryset):
        self.queryset = queryset

    @abstractmethod
    def calculate(self):
        pass

    def get_chart_builder_class(self):
        from analytics.charts.line_chart import LineChartBuilder
        return LineChartBuilder  # по умолчанию — LineChart