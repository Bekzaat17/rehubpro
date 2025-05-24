"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from users.views import consultant
from users.views.auth import LoginView
from users.views.dashboard import AdminPanelView, ConsultantDashboardView, PsychologistDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin_panel'),
    path('consultant/', consultant.dashboard, name='consultant_dashboard'),
    path('psychologist/', PsychologistDashboardView.as_view(), name='psychologist_dashboard'),]
