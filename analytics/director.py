# analytics/director.py

from analytics.filters import FilterAdapter

class ReportDirector:
    def __init__(self, queryset, filters: dict, metric_classes: list):
        self.queryset = queryset
        self.filters = filters
        self.metric_classes = metric_classes


    def run(self):
        filtered = FilterAdapter(self.filters).apply(self.queryset)
        results = {}

        for MetricClass in self.metric_classes:
            metric = MetricClass(filtered)
            data = metric.calculate()

            ChartBuilder = metric.get_chart_builder_class()
            chart = ChartBuilder().set_data(data).set_title(data.get("title", MetricClass.__name__)).build()

            results[MetricClass.__name__] = chart

        return results