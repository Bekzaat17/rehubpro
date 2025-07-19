from django.urls import path, include
from residents.views.add import AddResidentView
from residents.views.residents_data_view import ResidentsDataView
from rest_framework.routers import DefaultRouter
from residents.views.resident_profile_viewset import ResidentProfileViewSet

app_name = 'residents'


router = DefaultRouter()
router.register(r"residents", ResidentProfileViewSet, basename="resident")

urlpatterns = [
    path('add/', AddResidentView.as_view(), name='add'),
    path('data/', ResidentsDataView.as_view(), name='data'),
    path("api/", include(router.urls)),
]