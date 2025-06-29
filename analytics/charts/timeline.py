# analytics/charts/timeline.py

class TimelineBuilder:
    chart_type = "timeline"

    def __init__(self, data, title):
        self.data = data
        self.title = title

    def build(self):
        return {
            "type": self.chart_type,
            "title": self.title,
            "timeline": self.data.get("timeline", {})
        }