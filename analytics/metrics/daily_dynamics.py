# analytics/metrics/daily_dynamics.py

from collections import defaultdict
from .base import BaseMetric


class DailyDynamicsMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)

        for report in self.queryset.select_related("daily_dynamics"):
            dynamic = report.daily_dynamics
            if dynamic:
                score = getattr(dynamic, "score", None)
                if score is not None:
                    daily_scores[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        return {
            "title": "Дневная динамика (по score)",
            "data": averaged
        }