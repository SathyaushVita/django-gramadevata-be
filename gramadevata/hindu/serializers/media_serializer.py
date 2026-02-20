





from rest_framework import serializers
from ..models import Media
from django.conf import settings

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"

