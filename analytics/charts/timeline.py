# analytics/charts/timeline.py
from analytics.charts.base import BaseChartBuilder


class TimelineBuilder(BaseChartBuilder):
    def __init__(self):
        self._data = {}
        self._title = ""

    def set_data(self, data: dict):
        self._data = data
        return self

    def set_title(self, title: str):
        self._title = title
        return self

    def build(self):
        return {
            "type": "timeline",
            "title": self._title,
            "timeline": self._data.get("timeline", {})
        }