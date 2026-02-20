from rest_framework import serializers
from ..models import *


class TemplePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplePriority
        fields = "__all__"