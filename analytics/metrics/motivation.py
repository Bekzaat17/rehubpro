# analytics/metrics/motivation.py

from collections import defaultdict
from .base import BaseMetric

class MotivationMetric(BaseMetric):
    def calculate(self):
        data = defaultdict(list)
        for report in self.queryset:
            motivation = report.motivation
            if motivation:
                score = getattr(motivation, 'score', None)
                if score is not None:
                    data[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in data.items()
        }
        return averaged