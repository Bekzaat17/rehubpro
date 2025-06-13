# roles/views/assign_roles.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from residents.models import Resident
from roles.models.resident_role_assignment import ResidentRoleAssignment

class AssignRolesView(LoginRequiredMixin, TemplateView):
    template_name = "roles/assign_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Загружаем всех резидентов с текущими ролями
        residents = Resident.objects.all().prefetch_related("role_assignments__role")

        context["residents"] = residents
        return context