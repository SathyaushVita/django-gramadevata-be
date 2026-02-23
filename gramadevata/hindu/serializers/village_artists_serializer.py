from rest_framework import serializers
from ..models import VillageArtist
from django.utils.timesince import timesince
from django.utils import timezone
from rest_framework import serializers
from ..models import VillageArtist,Register
from ..utils import image_path_to_binary


class VillageArtistSerializer(serializers.ModelSerializer):
    artist_image = serializers.SerializerMethodField()
    traditional_occupation_pics = serializers.SerializerMethodField()
    traditional_occupation_video = serializers.SerializerMethodField()
    trained_under_pics = serializers.SerializerMethodField()
    audio_recordings = serializers.SerializerMethodField()

    def convert_paths(self, value):
        if isinstance(value, list):
            paths = value
        elif isinstance(value, str):
            paths = value.strip('[]').replace('"', '').split(',')
            paths = [p.strip() for p in paths if p.strip()]
        else:
            paths = []
        return [image_path_to_binary(p) for p in paths]

    def get_artist_image(self, instance):
        return self.convert_paths(instance.artist_image)

    def get_traditional_occupation_pics(self, instance):
        return self.convert_paths(instance.traditional_occupation_pics)

    def get_traditional_occupation_video(self, instance):
        return self.convert_paths(instance.traditional_occupation_video)

    def get_trained_under_pics(self, instance):
        return self.convert_paths(instance.trained_under_pics)

    def get_audio_recordings(self, instance):
        return self.convert_paths(instance.audio_recordings)

    class Meta:
        model = VillageArtist
        fields = '__all__'








class InactiveVillageArtistSerializer(serializers.ModelSerializer):
    artist_image = serializers.SerializerMethodField()
    traditional_occupation_pics = serializers.SerializerMethodField()
    traditional_occupation_video = serializers.SerializerMethodField()
    trained_under_pics = serializers.SerializerMethodField()
    audio_recordings = serializers.SerializerMethodField()
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
    def convert_paths(self, value):
        if isinstance(value, list):
            paths = value
        elif isinstance(value, str):
            paths = value.strip('[]').replace('"', '').split(',')
            paths = [p.strip() for p in paths if p.strip()]
        else:
            paths = []
        return [image_path_to_binary(p) for p in paths]

    def get_artist_image(self, instance):
        return self.convert_paths(instance.artist_image)

    def get_traditional_occupation_pics(self, instance):
        return self.convert_paths(instance.traditional_occupation_pics)

    def get_traditional_occupation_video(self, instance):
        return self.convert_paths(instance.traditional_occupation_video)

    def get_trained_under_pics(self, instance):
        return self.convert_paths(instance.trained_under_pics)

    def get_audio_recordings(self, instance):
        return self.convert_paths(instance.audio_recordings)

    class Meta:
        model = VillageArtist
        fields = '__all__'
