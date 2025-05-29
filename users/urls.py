# users/urls.py
from django.urls import path
from users.views.auth import LoginView
from users.views.dashboard import AdminPanelView, ConsultantDashboardView, PsychologistDashboardView
from users.views import consultant

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin_panel'),
    path('consultant/', consultant.dashboard, name='consultant_dashboard'),
    path('psychologist/', PsychologistDashboardView.as_view(), name='psychologist_dashboard'),
]