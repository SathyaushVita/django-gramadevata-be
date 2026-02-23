


from rest_framework import serializers
from ..models import VillageDevelopmentFacility,Register
from ..utils import image_path_to_binary  

from django.utils.timesince import timesince
from django.utils import timezone

class VillageDevelopmentFacilitySerializer(serializers.ModelSerializer):
    primarysource_of_livelihood_image = serializers.SerializerMethodField()

    class Meta:
        model = VillageDevelopmentFacility
        fields = '__all__'

    def get_primarysource_of_livelihood_image(self, obj):
        images = obj.primarysource_of_livelihood_image or []
        return [image_path_to_binary(img) for img in images]








class InactiveVillageDevelopmentFacilitySerializer(serializers.ModelSerializer):
    primarysource_of_livelihood_image = serializers.SerializerMethodField()
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
        model = VillageDevelopmentFacility
        fields = '__all__'

    def get_primarysource_of_livelihood_image(self, obj):
        images = obj.primarysource_of_livelihood_image or []
        return [image_path_to_binary(img) for img in images]