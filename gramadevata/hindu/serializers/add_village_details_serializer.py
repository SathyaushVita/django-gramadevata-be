from rest_framework import serializers
from ..models import AddVillageDetails, Media
from ..utils import image_path_to_binary
from django.conf import settings
from .media_serializer import MediaSerializer
class AddVillageDetailsSerializer(serializers.ModelSerializer):
    media_details = serializers.SerializerMethodField()
    class Meta:
        model = AddVillageDetails
        fields = "__all__"
        extra_kwargs = {'image_location': {'required': False, 'default': list}, 'village_video': {'required': False, 'default': list}}
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
        if instance.village_video:
            video_paths = (
                instance.village_video if isinstance(instance.village_video, list) else instance.village_video.strip('[]').replace('"', '').split(',')
            )
            representation['village_video'] = [f"{settings.FILE_URL}{path.strip()}" for path in video_paths]
        else:
            representation['village_video'] = []
        return representation
    # This is the method that needs to be defined for the SerializerMethodField
    def get_media_details(self, obj):
        media = Media.objects.filter(village_id=obj.village_id,status='ACTIVE')
        return MediaSerializer(media, many=True).data
