from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from residents.models import Resident
from residents.services.resident_profile_service import ResidentProfileService
from residents.serializers.resident_profile_serializer import ResidentProfileSerializer


class ResidentProfileViewSet(LoginRequiredMixin, viewsets.ViewSet):
    """
    API для отображения и редактирования личного дела резидента
    """

    @action(detail=True, methods=["get", "patch"], url_path="profile")
    def profile(self, request, pk=None):
        """
        GET — получить данные профиля резидента
        PATCH — обновить поля профиля (notes, dependency_type)
        """
        resident = Resident.objects.get(pk=pk)

        if request.method == "GET":
            data = ResidentProfileService.get_profile_data(resident)
            return Response(data)

        elif request.method == "PATCH":
            serializer = ResidentProfileSerializer(resident, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"detail": "Данные обновлены"})

    @action(detail=True, methods=["post"], url_path="discharge")
    def discharge(self, request, pk=None):
        """
        POST — завершить лечение (soft delete)
        """
        resident = Resident.objects.get(pk=pk)
        ResidentProfileService.soft_delete(resident)
        return Response({"detail": "Лечение завершено"}, status=status.HTTP_200_OK)