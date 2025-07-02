from analytics.charts.base import BaseChartBuilder


class HeatmapBuilder(BaseChartBuilder):
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
            "type": "heatmap",
            "title": self._title,
            "rows": self._data.get("rows", []),
            "columns": self._data.get("columns", []),
            "values": self._data.get("values", [])
        }