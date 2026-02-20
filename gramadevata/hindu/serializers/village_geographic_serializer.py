# serializers.py
from rest_framework import serializers
from ..models import Geographic

class VillageGeographicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geographic
        fields = '__all__'
