from rest_framework import serializers
from ..models import PujariCategory


class PujariCategeorySerializer(serializers.ModelSerializer):
     class Meta:
          model = PujariCategory
          fields = ["_id","name"]