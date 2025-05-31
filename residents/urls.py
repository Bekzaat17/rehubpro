from django.urls import path
from residents.views.add import AddResidentView
from residents.views.residents_data_view import ResidentsDataView

app_name = 'residents'

urlpatterns = [
    path('add/', AddResidentView.as_view(), name='add'),
    path('data/', ResidentsDataView.as_view(), name='data'),
]