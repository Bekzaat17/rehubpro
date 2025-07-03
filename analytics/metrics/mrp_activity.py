# analytics/metrics/mrp_activity.py

from collections import defaultdict
from .base import BaseMetric

class MRPActivityMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)

        for report in self.queryset.select_related("mrp_activity"):
            activity = report.mrp_activity
            if activity:
                score = getattr(activity, "score", None)
                if score is not None:
                    daily_scores[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        return {
            "title": "Активность на занятиях MRP (по score)",
            "labels": list(map(str, averaged.keys())),
            "values": list(averaged.values())
        }