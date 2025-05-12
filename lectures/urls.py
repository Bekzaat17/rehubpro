# lectures/urls.py

from django.urls import path
from lectures.views.lecture_list_view import lecture_list_view
from lectures.views.lecture_detail_view import lecture_detail_view

urlpatterns = [
    path('', lecture_list_view, name='lecture_list'),
    path('<int:pk>/', lecture_detail_view, name='lecture_detail'),
]