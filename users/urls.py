# users/urls.py
from django.urls import path
from users.views.auth import LoginView
from users.views.consultant_dashboard_view import ConsultantDashboardView

app_name = 'users'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', ConsultantDashboardView.as_view(), name='dashboard'),
]