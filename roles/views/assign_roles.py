# roles/views/assign_roles.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from residents.models import Resident


class AssignRolesView(LoginRequiredMixin, TemplateView):
    template_name = "roles/assign_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Загружаем всех резидентов с их назначениями и ролями
        residents = Resident.active.all().prefetch_related("role_assignments__role")

        # Добавляем каждому резиденту поле `active_roles`
        for resident in residents:
            resident.active_roles = resident.role_assignments.filter(unassigned_at__isnull=True)

        context["residents"] = residents
        return context