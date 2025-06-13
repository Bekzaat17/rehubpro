# roles/views/resident_role_modal.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

from residents.models import Resident
from roles.models.resident_role_assignment import ResidentRoleAssignment, ResidentRole


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ResidentRoleModalView(LoginRequiredMixin, View):
    def get(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        assignments = ResidentRoleAssignment.objects.filter(resident=resident).order_by('-assigned_at')
        return render(request, "roles/role_modal_content.html", {
            "resident": resident,
            "active_roles": assignments.filter(unassigned_at__isnull=True),
            "history": assignments,
            "available_roles": ResidentRole.objects.all().order_by("name")
        })

    def post(self, request, resident_id):
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseBadRequest("Not AJAX")

        resident = get_object_or_404(Resident, id=resident_id)
        action = request.POST.get("action")

        if action == "assign":
            role_id = request.POST.get("role_id")
            if not role_id:
                return JsonResponse({"success": False, "message": "Роль не выбрана"})
            role = get_object_or_404(ResidentRole, id=role_id)
            ResidentRoleAssignment.objects.create(resident=resident, role=role)
            return JsonResponse({"success": True})

        elif action == "end":
            assignment_id = request.POST.get("assignment_id")
            if not assignment_id:
                return JsonResponse({"success": False, "message": "Назначение не найдено"})
            assignment = get_object_or_404(ResidentRoleAssignment, id=assignment_id, resident=resident)
            assignment.unassigned_at = timezone.now()
            comment = request.POST.get("comment", "").strip()
            if comment:
                assignment.comment = comment
            assignment.save()
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "message": "Неизвестное действие"})