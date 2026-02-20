from rest_framework import serializers
from ..models import AddEventDetails,Media
from ..utils import image_path_to_binary
from django.conf import settings
from .media_serializer import MediaSerializer


class AddEventDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddEventDetails
        fields = "__all__"
        extra_kwargs = {'image_location': {'required': False, 'default': list}, 'event_video': {'required': False, 'default': list}}
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
        if instance.event_video:
            video_paths = (
                instance.event_video if isinstance(instance.event_video, list) else instance.event_video.strip('[]').replace('"', '').split(',')
            )
            representation['event_video'] = [f"{settings.FILE_URL}{path.strip()}" for path in video_paths]
        else:
            representation['event_video'] = []
        return representation
    def get_media_details(self, obj):
        media = Media.objects.filter(event_id=obj.event_id,status='ACTIVE')
        return MediaSerializer(media, many=True).data