# analytics/filters.py

class FilterAdapter:
    def __init__(self, params: dict):
        self.params = params

    def apply(self, queryset, date_field: str = "date"):
        date_from = self.params.get("date_from")
        date_to = self.params.get("date_to")
        resident_id = self.params.get("resident_id")

        if date_from:
            queryset = queryset.filter(**{f"{date_field}__gte": date_from})
        if date_to:
            queryset = queryset.filter(**{f"{date_field}__lte": date_to})

        if resident_id:
            model_name = queryset.model._meta.model_name

            if model_name == "residentreport":
                queryset = queryset.filter(resident_id=resident_id)
            elif model_name == "taskprogress":
                queryset = queryset.filter(assigned_task__resident_id=resident_id)

        return queryset