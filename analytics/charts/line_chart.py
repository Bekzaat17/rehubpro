# analytics/charts/line_chart.py

class LineChartBuilder:
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
            "labels": list(map(str, self._data.keys())),  # даты как строки
            "values": list(self._data.values()),
        }