# analytics/charts/pie_chart.py
from analytics.charts.base import BaseChartBuilder


class PieChartBuilder(BaseChartBuilder):
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
            "type": "pie",
            "title": self._title,
            "labels": self._data.get("labels", []),
            "values": self._data.get("values", []),
        }