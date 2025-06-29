# analytics/metrics/usts_format_followed.py

from collections import Counter
from .base import BaseMetric
from analytics.charts.bar_chart import BarChartBuilder

class USTSFormatFollowedMetric(BaseMetric):
    def calculate(self):
        counter = Counter()
        for report in self.queryset:
            key = "Да" if report.usts_format_followed else "Нет"
            counter[key] += 1

        return {
            "title": "Соблюдение формата УЦСТ",
            "labels": list(counter.keys()),
            "values": list(counter.values())
        }

    def get_chart_builder_class(self):
        return BarChartBuilder