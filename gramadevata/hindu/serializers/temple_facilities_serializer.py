
from rest_framework import serializers
from ..models import TempleFacilities

class TempleFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleFacilities
        fields = '__all__'
