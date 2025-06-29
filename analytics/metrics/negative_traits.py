# analytics/metrics/negative_traits.py

from collections import Counter, defaultdict
from .base import BaseMetric
from analytics.charts.pie_chart import PieChartBuilder

class NegativeTraitsMetric(BaseMetric):
    def calculate(self):
        trait_counter = Counter()
        trait_scores = defaultdict(int)

        for report in self.queryset.prefetch_related("negative_traits"):
            for trait in report.negative_traits.all():
                trait_counter[trait.name] += 1
                trait_scores[trait.name] += getattr(trait, "score", 0)

        top_traits = trait_counter.most_common(5)

        return {
            "title": "Негативные черты (частота)",
            "labels": [trait for trait, _ in top_traits],
            "values": [count for _, count in top_traits]
        }

    def get_chart_builder_class(self):
        return PieChartBuilder