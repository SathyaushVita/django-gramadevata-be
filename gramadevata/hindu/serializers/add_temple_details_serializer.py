from rest_framework import serializers
from ..models import AddTempleDetails,Media
from ..utils import image_path_to_binary
from django.conf import settings
from .media_serializer import MediaSerializer





class AddTempleDetailsSerializer(serializers.ModelSerializer):
    media_details = serializers.SerializerMethodField()

    class Meta:
        model = AddTempleDetails
        fields = "__all__"
        extra_kwargs = {'image_location': {'required': False, 'default': list}, 'video': {'required': False, 'default': list}}

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
        if instance.video:
            video_paths = (
                instance.video if isinstance(instance.video, list) else instance.video.strip('[]').replace('"', '').split(',')
            )
            representation['video'] = [f"{settings.FILE_URL}{path.strip()}" for path in video_paths]
        else:
            representation['video'] = []

        return representation
    def get_media_details(self, obj):
        media = Media.objects.filter(temple_id=obj.temple_id, status='ACTIVE')
        return MediaSerializer(media, many=True).data









    