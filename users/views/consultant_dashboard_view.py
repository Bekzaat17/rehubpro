# users/views/consultant_dashboard_view.py

from django.views.generic import TemplateView
from residents.forms import ResidentForm


class ConsultantDashboardView(TemplateView):
    """
    Представление для пустого личного кабинета консультанта.
    Заглушка, которая будет дополняться модулями (таблицами, окнами и т.п.).
    """
    template_name = 'users/consultant_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResidentForm()  # ← добавляем форму
        return context