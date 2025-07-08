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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Подключаем все маршруты из users
    path('residents/', include('residents.urls', namespace='residents')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path("roles/", include("roles.urls", namespace="roles")),
    path("reports/", include("reports.urls",  namespace="reports")),
    path("references/", include("references.urls", namespace="references")),
    path("analytics/", include("analytics.urls", namespace="analytics")),
    path("storage/", include("storage.urls", namespace="storage"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO vyvesti media za root
