
from rest_framework import serializers
from ..models import SocialActivity

class SocialActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialActivity
        fields = '__all__'
