# analytics/metrics/family_activity.py

from collections import defaultdict
from .base import BaseMetric
from analytics.charts.line_chart import LineChartBuilder

class FamilyActivityMetric(BaseMetric):
    def calculate(self):
        daily_scores = defaultdict(list)

        for report in self.queryset.select_related("family_activity"):
            activity = report.family_activity
            if activity:
                score = getattr(activity, "score", None)
                if score is not None:
                    daily_scores[report.date].append(score)

        averaged = {
            date: round(sum(scores) / len(scores), 2)
            for date, scores in daily_scores.items()
        }

        return {
            "title": "Семейная активность (по score)",
            "labels": list(map(str, averaged.keys())),
            "values": list(averaged.values())
        }

    def get_chart_builder_class(self):
        return LineChartBuilder