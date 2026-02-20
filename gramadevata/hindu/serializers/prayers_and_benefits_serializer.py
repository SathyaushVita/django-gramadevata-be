# your_app/serializers.py

from rest_framework import serializers
from ..models import PrayersAndBenefits

class PrayersAndBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayersAndBenefits
        fields = '__all__'
