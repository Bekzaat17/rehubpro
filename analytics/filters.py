# analytics/filters.py

class FilterAdapter:
    def __init__(self, params: dict):
        self.params = params

    def apply(self, queryset):
        date_from = self.params.get("date_from")
        date_to = self.params.get("date_to")
        resident = self.params.get("resident")

        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if resident:
            queryset = queryset.filter(resident=resident)
        return queryset