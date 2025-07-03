# analytics/director.py

from analytics.filters import FilterAdapter

class ReportDirector:
    def __init__(self, queryset, filters: dict, metric_classes: list):
        self.queryset = queryset
        self.filters = filters
        self.metric_classes = metric_classes

    def run(self):
        results = {}

        for MetricClass in self.metric_classes:
            base_queryset = MetricClass.get_base_queryset(self.filters)
            date_field = MetricClass.get_filter_field()
            filtered = FilterAdapter(self.filters).apply(base_queryset, date_field=date_field)

            metric = MetricClass(filtered)
            data = metric.calculate()

            ChartBuilder = metric.get_chart_builder_class()
            chart = ChartBuilder().set_data(data).set_title(data.get("title", MetricClass.__name__)).build()

            results[MetricClass.__name__] = chart

        return results