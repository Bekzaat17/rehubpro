# analytics/charts/bar_chart.py
from analytics.charts.base import BaseChartBuilder


class BarChartBuilder(BaseChartBuilder):
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
            "type": "bar",
            "title": self._title,
            "labels": self._data["labels"],
            "values": self._data["values"]
        }