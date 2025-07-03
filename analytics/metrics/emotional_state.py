# analytics/metrics/emotional_state.py

from collections import defaultdict
from .base import BaseMetric

class EmotionalStateMetric(BaseMetric):
    def calculate(self):
        data = defaultdict(list)
        for report in self.queryset:
            state = report.emotional_state
            if state:
                score = getattr(state, 'score', None)
                if score is not None:
                    data[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in data.items()
        }

        return {
            "title": "Эмоциональное состояние (по score)",
            "data": averaged
        }