from rest_framework import serializers
from .models import Capitulo

class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'

