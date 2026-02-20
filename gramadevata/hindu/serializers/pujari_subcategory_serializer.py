from rest_framework import serializers
from ..models import PujariSubCategory

class PujariSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PujariSubCategory
        fields = ['_id', 'name', 'category']  