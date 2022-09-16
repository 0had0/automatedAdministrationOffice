from rest_framework import serializers

from auth.serializers import AccountSerializer

from .models import (Institution,)


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = '__all__'

    def create(self):
        return Institution.objects.create(**self.data)
