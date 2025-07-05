# analytics/metrics/emotional_state.py

from collections import defaultdict
from .base import BaseMetric

class EmotionalStateMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)

        for report in self.queryset.select_related("emotional_state"):
            state = report.emotional_state
            if state:
                score = getattr(state, 'score', None)
                if score is not None:
                    daily_scores[report.date].append(score)

        # усреднённые значения по дате
        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        # сортируем по дате
        sorted_dates = sorted(averaged.keys())
        labels = [str(date) for date in sorted_dates]
        values = [averaged[date] for date in sorted_dates]

        return {
            "title": "Эмоциональное состояние (по score)",
            "labels": labels,
            "values": values
        }