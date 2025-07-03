# analytics/charts/line_chart.py
from analytics.charts.base import BaseChartBuilder


class LineChartBuilder(BaseChartBuilder):
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
            "type": "line",
            "title": self._title,
            "labels": self._data.get("labels", []),
            "values": self._data.get("values", []),
        }