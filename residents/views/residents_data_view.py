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

        # Названия колонок (можно потом расширить — динамически)
        column_names = [
            "ФИО",
            "Дата рождения",
            "Дата поступления",
            "Тип зависимости",
            "Заметки"
        ]

        data = []
        for resident in residents:
            data.append([
                resident.full_name,
                format_date(resident.date_of_birth),
                format_date(resident.date_of_admission),
                resident.get_dependency_type_display() if resident.dependency_type else "—",
                resident.notes or "—"
            ])

        return JsonResponse({
            "columns": column_names,
            "rows": data
        })