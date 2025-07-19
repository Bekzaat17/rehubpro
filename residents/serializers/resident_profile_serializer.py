from rest_framework import serializers
from residents.models import Resident


class ResidentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ["notes", "dependency_type"]