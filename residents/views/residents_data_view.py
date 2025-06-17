# residents/views/residents_data_view.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
# from residents.models import Resident # Replaced by service
from core.util import format_date

from residents.services.resident_service import DefaultResidentService
from residents.repositories.resident_repository import DjangoResidentRepository


class ResidentsDataView(LoginRequiredMixin, View):
    """
    API-представление, возвращающее список резидентов в виде JSON.
    Все названия колонок и значения динамически формируются.
    """
    resident_service: DefaultResidentService # Type hint for service instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate repository and service
        # In a more complex app with DI framework, these would be injected.
        resident_repository = DjangoResidentRepository()
        self.resident_service = DefaultResidentService(resident_repository=resident_repository)

    def get(self, request):
        # Use the service to get residents
        residents = self.resident_service.get_all_residents()

        # Названия колонок (можно потом расширить — динамически)
        column_names = [
            "ФИО",
            "Дата рождения",
            "Дата поступления",
            "Тип зависимости",
            "Заметки"
        ]

        data = []
        for resident in residents: # residents is now a list/sequence from the service
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