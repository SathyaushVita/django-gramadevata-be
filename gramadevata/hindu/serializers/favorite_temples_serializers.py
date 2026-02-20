
from rest_framework import serializers
from ..models import FavoriteTemple
from ..utils import image_path_to_binary  

class FavoriteTempleSerializer(serializers.ModelSerializer):
    # Temple fields
    temple_name = serializers.CharField(source='temple_id.name', read_only=True)
    temple_image = serializers.SerializerMethodField()

    # Goshala fields
    goshala_name = serializers.CharField(source='goshala_id.name', read_only=True)
    goshala_image = serializers.SerializerMethodField()

    # Event fields
    event_name = serializers.CharField(source='event_id.name', read_only=True)
    event_image = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteTemple
        fields = [
            '_id', 'user_id', 'temple_id', 'created_at',
            'temple_name', 'temple_image',
            'event_id', 'event_name', 'event_image',
            'goshala_id', 'goshala_name', 'goshala_image'
        ]

    # TEMPLE IMAGE
    def get_temple_image(self, instance):
        return self._extract_image(instance.temple_id.image_location if instance.temple_id else None)

    # GOSHALA IMAGE
    def get_goshala_image(self, instance):
        return self._extract_image(instance.goshala_id.image_location if instance.goshala_id else None)

    # EVENT IMAGE
    def get_event_image(self, instance):
        return self._extract_image(instance.event_id.image_location if instance.event_id else None)

    # HELPER FUNCTION
    def _extract_image(self, filename):
        if not filename:
            return None

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            filename = filename.strip('[]').replace('"', '')
            image_paths = [path.strip() for path in filename.split(',')]
        else:
            image_paths = []

        if not image_paths:
            return None

        return image_path_to_binary(image_paths[0])
