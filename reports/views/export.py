from django.http import HttpResponse
from django.views import View
from django.utils.dateparse import parse_date
from reports.models.resident_report import ResidentReport
from django.template.loader import render_to_string
from weasyprint import HTML

#TODO dobavit logo v export_pdf

class ExportReportsView(View):
    """
    Экспорт всех отчётов за выбранную дату в формате TXT.
    """

    def get(self, request):
        export_format = request.GET.get("format", "txt")
        date_str = request.GET.get("date")

        if not date_str:
            return HttpResponse("Дата не указана.", status=400)

        selected_date = parse_date(date_str)
        if not selected_date:
            return HttpResponse("Неверный формат даты.", status=400)

        reports = ResidentReport.objects.filter(date=selected_date) \
            .select_related(
            "resident",
            "emotional_state",
            "physical_state",
            "motivation",
            "daily_dynamics",
            "mrp_activity",
            "family_activity"
        ).prefetch_related(
            "positive_traits",
            "negative_traits",
            "task_comments__assigned_task",
            "role_statuses__role_assignment__role"
        )

        # подготавливаем данные как в view_reports_by_date
        prepared_reports = []
        for report in reports:
            task_comments = {
                tc.assigned_task.task.title: tc.comment
                for tc in report.task_comments.all()
            }
            role_statuses = {
                rs.role_assignment.role.name: rs.get_status_display()
                for rs in report.role_statuses.all()
            }

            prepared_reports.append({
                "resident": report.resident,
                "emotional_state": str(report.emotional_state) if report.emotional_state else "—",
                "physical_state": str(report.physical_state) if report.physical_state else "—",
                "motivation": str(report.motivation) if report.motivation else "—",
                "daily_dynamics": str(report.daily_dynamics) if report.daily_dynamics else "—",
                "mrp_activity": str(report.mrp_activity) if report.mrp_activity else "—",
                "family_activity": str(report.family_activity) if report.family_activity else "—",
                "positive_traits": ", ".join(t.name for t in report.positive_traits.all()) or "—",
                "negative_traits": ", ".join(t.name for t in report.negative_traits.all()) or "—",
                "usts_info_shared": "Да" if report.usts_info_shared else "Нет",
                "usts_format_followed": "Да" if report.usts_format_followed else "Нет",
                "usts_comment": report.usts_comment or "—",
                "comment": report.comment or "—",
                "task_comments": task_comments,
                "role_statuses": role_statuses,
            })

        if export_format == "txt":
            return self._export_txt(prepared_reports, selected_date)
        elif export_format == "pdf":
            return self._export_pdf(prepared_reports, selected_date)
        else:
            return HttpResponse("Формат не поддерживается.", status=400)

    def _export_txt(self, reports, selected_date):
        content = [f"Отчёты за {selected_date.strftime('%d.%m.%Y')}\n"]
        content.append("=" * 40 + "\n")

        for i, report in enumerate(reports, 1):
            resident = report["resident"].full_name
            content.append(f"{i}. Резидент: {resident}")
            content.append(f"   Эмоциональное состояние: {report['emotional_state']}")
            content.append(f"   Физическое состояние: {report['physical_state']}")
            content.append(f"   Мотивация: {report['motivation']}")
            content.append(f"   Динамика: {report['daily_dynamics']}")
            content.append(f"   Активность на МРП: {report['mrp_activity']}")
            content.append(f"   Активность в семье: {report['family_activity']}")
            content.append(f"   🌱 Позитивные черты: {report['positive_traits']}")
            content.append(f"   ⚠️ Негативные черты: {report['negative_traits']}")
            content.append(f"   📌 УСТС — Информацию подавал: {report['usts_info_shared']}")
            content.append(f"   📌 УСТС — Формат соблюдён: {report['usts_format_followed']}")
            content.append(f"   📌 Комментарий по УСТС: {report['usts_comment']}")
            content.append(f"   💬 Общий комментарий: {report['comment']}")

            task_comments = report.get("task_comments", {})
            if task_comments:
                content.append("   🗂 Комментарии по задачам:")
                for task_name, comment in task_comments.items():
                    content.append(f"     - {task_name}: {comment}")

            role_statuses = report.get("role_statuses", {})
            if role_statuses:
                content.append("   👔 Статусы по функции:")
                for role_name, status in role_statuses.items():
                    content.append(f"     - {role_name}: {status}")

            content.append("\n" + "-" * 40 + "\n")

        txt_content = "\n".join(content)

        response = HttpResponse(txt_content, content_type="text/plain; charset=utf-8")
        filename = f"reports_{selected_date.strftime('%Y%m%d')}.txt"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    def _export_pdf(self, reports, selected_date):
        html_string = render_to_string("reports/export_pdf.html", {
            "reports": reports,
            "selected_date": selected_date
        })
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        filename = f"reports_{selected_date.strftime('%Y%m%d')}.pdf"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
