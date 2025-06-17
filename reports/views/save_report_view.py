# reports/views/save_report_view.py

from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError

from reports.models.resident_report import ResidentReport
# from reports.forms.resident_report_form import ResidentReportForm # Factory will provide this
from reports.services.report_validator import ReportValidator
from reports.factories.resident_report_form_factory import ResidentReportFormFactory


class SaveReportView(View):
    """
    Сохраняет отчёт по резиденту (AJAX).
    Только на текущую дату.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Instantiate the factory once if it's stateless or stores repos internally
        self.form_factory = ResidentReportFormFactory()

    def post(self, request, report_id):
        try:
            report = ResidentReport.objects.get(id=report_id)
        except ResidentReport.DoesNotExist:
            return JsonResponse({"success": False, "errors": "Отчёт не найден."}, status=404)

        if report.date != timezone.localdate():
            return JsonResponse({
                "success": False,
                "errors": "Редактирование отчёта возможно только в день заполнения."
            })

        # Use the factory to create the form
        form = self.form_factory.create(
            resident=report.resident,
            date=report.date,
            request_data=request.POST # Pass request.POST for bound form
        )

        if form.is_valid():
            # 💾 Сохраняем через фабрику (создаст или обновит)
            updated_report = form.save(created_by=request.user)

            # ✅ Валидация заполненности
            validator = ReportValidator(updated_report)

            try:
                validator.validate_post_creation(updated_report)
            except ValidationError as e:
                return JsonResponse({"success": False, "errors": str(e)}, status=400)

            return JsonResponse({"success": True})
        else:
            # Ensure form.errors is serializable for JsonResponse
            errors = form.errors.as_json() if hasattr(form.errors, 'as_json') else str(form.errors)
            return JsonResponse({"success": False, "errors": errors}, status=400)