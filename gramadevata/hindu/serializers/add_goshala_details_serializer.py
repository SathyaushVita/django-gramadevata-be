from rest_framework import serializers
from ..models import AddGoshalaDetails
from ..utils import image_path_to_binary
from django.conf import settings



class AddGoshalaDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddGoshalaDetails
        fields = "__all__"
        extra_kwargs = {'image_location': {'required': False, 'default': list}, 'goshala_video': {'required': False, 'default': list}}
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Handle image locations
        if instance.image_location:
            image_locations = (
                instance.image_location
                if isinstance(instance.image_location, list)
                else instance.image_location.strip('[]').replace('"', '').split(',')
            )
            representation['image_location'] = [f"{settings.FILE_URL}{path.strip()}" for path in image_locations]
        else:
            representation['image_location'] = []
        # Handle video locations
        if instance.goshala_video:
            video_paths = (
                instance.goshala_video if isinstance(instance.goshala_video, list) else instance.goshala_video.strip('[]').replace('"', '').split(',')
            )
            representation['goshala_video'] = [f"{settings.FILE_URL}{path.strip()}" for path in video_paths]
        else:
            representation['goshala_video'] = []
        return representation
