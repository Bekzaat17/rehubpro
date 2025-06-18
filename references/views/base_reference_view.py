from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class BaseReferenceView(LoginRequiredMixin, View):
    """
    Базовый view-класс для обработки CRUD запросов справочников.
    Реализует паттерн Template Method — шаблон поведения.
    """

    model = None          # Указывается в дочерних классах
    form_class = None     # Указывается в дочерних классах

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)

    def get(self, request):
        """
        Возвращает список всех активных элементов справочника.
        """
        data = list(self.get_queryset().values())
        return JsonResponse({'data': data})

    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        Обработка создания или обновления элемента.
        """
        from django.http import QueryDict
        data = QueryDict(request.body).dict()
        instance = None

        if data.get("id"):
            instance = get_object_or_404(self.model, id=data["id"])
            form = self.form_class(data, instance=instance)
        else:
            form = self.form_class(data)

        if form.is_valid():
            obj = form.save()
            return JsonResponse({"success": True, "item": model_to_dict(obj)})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    @method_decorator(csrf_exempt)
    def delete(self, request):
        """
        Soft-delete элемента справочника.
        """
        import json
        data = json.loads(request.body)
        obj = get_object_or_404(self.model, id=data["id"])
        obj.is_active = False
        obj.save()
        return JsonResponse({"success": True})