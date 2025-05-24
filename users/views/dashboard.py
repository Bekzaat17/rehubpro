# users/views/dashboard.py

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='dispatch')
class AdminPanelView(View):
    def get(self, request):
        return HttpResponse("<h2>Админ-панель</h2>")


@method_decorator(login_required, name='dispatch')
class ConsultantDashboardView(View):
    def get(self, request):
        return HttpResponse("<h2>Кабинет консультанта</h2>")


@method_decorator(login_required, name='dispatch')
class PsychologistDashboardView(View):
    def get(self, request):
        return HttpResponse("<h2>Кабинет психолога</h2>")