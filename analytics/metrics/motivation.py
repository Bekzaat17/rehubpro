# analytics/metrics/motivation.py

from collections import defaultdict
from .base import BaseMetric

class MotivationMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)

        for report in self.queryset.select_related("motivation"):
            motivation = report.motivation
            if motivation:
                score = getattr(motivation, "score", None)
                if score is not None:
                    daily_scores[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        return {
            "title": "Мотивация (по score)",
            "labels": list(map(str, averaged.keys())),
            "values": list(averaged.values())
        }