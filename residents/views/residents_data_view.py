# residents/views/residents_data_view.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from residents.models import Resident
from core.util import format_date


class ResidentsDataView(LoginRequiredMixin, View):
    """
    API-представление, возвращающее список резидентов в виде JSON.
    Все названия колонок и значения динамически формируются.
    """

    def get(self, request):
        residents = Resident.objects.all()

        column_names = [
            "ФИО",
            "Дата рождения",
            "Дата поступления",
            "Тип зависимости",
            "Заметки"
        ]

        data = []
        for r in residents:
            full_name = f"{r.last_name} {r.first_name} {r.middle_name or ''}".strip()
            data.append([
                full_name,
                format_date(r.date_of_birth),
                format_date(r.date_of_admission),
                r.get_dependency_type_display() if r.dependency_type else "—",
                r.notes or "—"
            ])

        return JsonResponse({
            "columns": column_names,
            "rows": data
        })