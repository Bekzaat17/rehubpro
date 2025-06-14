# reports/views/save_report_view.py

from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError

from reports.models.resident_report import ResidentReport
from reports.forms.resident_report_form import ResidentReportForm
from reports.services.report_validator import ReportValidator


class SaveReportView(View):
    """
    Сохраняет отчёт по резиденту (AJAX).
    Только на текущую дату.
    """

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

        # 🔧 Используем резидента и дату из существующего отчёта
        form = ResidentReportForm(
            request.POST,
            resident=report.resident,
            date=report.date
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
            return JsonResponse({"success": False, "errors": form.errors}, status=400)