from rest_framework import serializers
from ..models import TemplePoojaTiming

class TemplePoojaTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplePoojaTiming
        fields = '__all__'
