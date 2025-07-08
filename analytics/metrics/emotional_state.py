# analytics/metrics/emotional_state.py

from collections import defaultdict
from .base import BaseMetric

class EmotionalStateMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)
        daily_names = defaultdict(list)

        for report in self.queryset.select_related("emotional_state"):
            state = report.emotional_state
            if state:
                score = getattr(state, 'score', None)
                name = getattr(state, 'name', None)  # "Ровное", "Агрессивное", и т.д.
                if score is not None:
                    daily_scores[report.date].append(score)
                    if name:
                        daily_names[report.date].append(name)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        sorted_dates = sorted(averaged.keys())
        labels = [str(date) for date in sorted_dates]

        values = [averaged[date] for date in sorted_dates]

        value_labels = [
            f"{averaged[date]} ({max(set(daily_names[date]), key=daily_names[date].count)})"
            if daily_names[date]
            else str(averaged[date])
            for date in sorted_dates
        ]

        return {
            "title": "Эмоциональное состояние",
            "labels": labels,
            "values": values,
            "value_labels": value_labels,  # 👈 для tooltip'ов
        }