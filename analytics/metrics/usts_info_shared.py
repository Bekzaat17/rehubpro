# analytics/metrics/usts_info_shared.py

from collections import Counter
from .base import BaseMetric
from analytics.charts.bar_chart import BarChartBuilder

class USTSInfoSharedMetric(BaseMetric):
    def calculate(self):
        counter = Counter()
        for report in self.queryset:
            key = "Да" if report.usts_info_shared else "Нет"
            counter[key] += 1

        return {
            "title": "Информацию подает и принимает на ровных чувствах УСТС",
            "labels": list(counter.keys()),
            "values": list(counter.values())
        }

    def get_chart_builder_class(self):
        return BarChartBuilder