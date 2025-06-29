# analytics/metrics/resident_role_responsibility.py


from collections import defaultdict
from .base import BaseMetric
from analytics.charts.heatmap import HeatmapBuilder


class ResidentRoleResponsibilityMetric(BaseMetric):
    """
    Heatmap-метрика: по каким ролям в какие дни резидент был ответственным или безответственным.
    """

    def calculate(self):
        # Формат: {(role_name, date): status}
        raw_data = {}
        roles = set()
        dates = set()

        # Prefetch — чтобы не было лишних запросов
        queryset = self.queryset.prefetch_related(
            "role_statuses__role_assignment__role"
        )

        for report in queryset:
            date = str(report.date)  # строка для JSON-ключей
            dates.add(date)

            for status in report.role_statuses.all():
                role = status.role_assignment.role
                if role is None:
                    continue  # пропускаем удалённые роли
                role_name = role.name
                roles.add(role_name)
                raw_data[(role_name, date)] = status.status

        # Упорядочиваем
        sorted_roles = sorted(roles)
        sorted_dates = sorted(dates)

        # Строим values: список строк (по ролям), внутри — список статусов по датам
        values = []
        for role in sorted_roles:
            row = []
            for date in sorted_dates:
                row.append(raw_data.get((role, date)))  # либо status, либо None
            values.append(row)

        return {
            "title": "Ответственность по ролям",
            "rows": sorted_roles,
            "columns": sorted_dates,
            "values": values
        }

    def get_chart_builder_class(self):
        return HeatmapBuilder