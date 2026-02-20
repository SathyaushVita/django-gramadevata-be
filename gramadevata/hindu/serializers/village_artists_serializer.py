# serializers.py
from rest_framework import serializers
from ..models import VillageArtist



# serializers.py
from rest_framework import serializers
from ..models import VillageArtist
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
