from rest_framework import serializers
from ..models import TempleTransport,Register

from django.utils.timesince import timesince
from django.utils import timezone

class TempleTransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleTransport
        fields = '__all__'



class InactiveTransportSerializer(serializers.ModelSerializer):

    user_full_name = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()

    def get_relative_time(self, instance):
        if not instance.created_at:
            return None

        now = timezone.now()
        diff = timesince(instance.created_at, now)

        return f"{diff} ago"

    def get_user_full_name(self, instance):
        try:
            if instance.user_id:
                return instance.user_id.full_name
        except Register.DoesNotExist:
            return None
        return None



    class Meta:
        model = TempleTransport
        fields = '__all__'
