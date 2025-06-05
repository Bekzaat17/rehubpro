# users/urls.py
from django.urls import path
from users.views.auth import LoginView
from users.views.consultant_dashboard_view import ConsultantDashboardView
from users.views.logout_view import LogoutView
from users.views.settings_view import UserSettingsView

app_name = 'users'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', ConsultantDashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/settings/', UserSettingsView.as_view(), name='settings'),
]