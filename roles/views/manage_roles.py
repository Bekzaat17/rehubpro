# roles/views/manage_roles.py
import json
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, QueryDict, Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.utils.decorators import classonlymethod
from django.shortcuts import get_object_or_404
from references.models.resident_role import ResidentRole


class ManageRolesView(LoginRequiredMixin, TemplateView):
    """
    Отображает страницу управления справочником ролей резидентов.
    """
    template_name = "roles/manage_roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resident_roles"] = ResidentRole.objects.all().order_by("name")
        return context


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ManageRolesApiView(LoginRequiredMixin, View):
    """
    Обработка API-запросов для управления ролями резидентов.
    """

    def post(self, request):
        """
        Создание новой роли.
        """
        name = request.POST.get("name", "").strip()
        slug = request.POST.get("slug", "").strip()
        description = request.POST.get("description", "").strip()

        if not name:
            return JsonResponse({"error": "Поле 'name' обязательно"}, status=400)

        role = ResidentRole.objects.create(name=name, slug=slug, description=description)
        return JsonResponse({"id": str(role.id), "status": "created"})

    def put(self, request, *args, **kwargs):
        """
        Обновление существующей роли.
        """
        pk = kwargs.get("pk")
        role = self.get_object(pk)

        if request.content_type == "application/x-www-form-urlencoded":
            data = QueryDict(request.body)
        else:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Неверный JSON"}, status=400)

        name = data.get("name", "").strip()
        slug = data.get("slug", "").strip()
        description = data.get("description", "").strip()

        if not name:
            return JsonResponse({"error": "Поле 'name' обязательно"}, status=400)

        role.name = name
        role.slug = slug
        role.description = description
        role.save()

        return JsonResponse({"status": "updated"})

    def delete(self, request, *args, **kwargs):
        """
        Удаление роли.
        """
        pk = kwargs.get("pk")
        role = self.get_object(pk)
        role.delete()
        return JsonResponse({"status": "deleted"})

    def get_object(self, pk):
        """
        Получение роли по UUID с 404, если не найдена.
        """
        import uuid
        from django.http import Http404

        if isinstance(pk, str):
            try:
                pk = uuid.UUID(pk)
            except ValueError:
                raise Http404("Неверный UUID")

        return get_object_or_404(ResidentRole, pk=pk)