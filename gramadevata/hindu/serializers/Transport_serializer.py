from rest_framework import serializers
from ..models import TempleTransport

class TempleTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleTransport
        fields = '__all__'
