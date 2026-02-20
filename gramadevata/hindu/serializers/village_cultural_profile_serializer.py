from rest_framework import serializers
from ..models import VillageCulturalProfile
from ..utils import image_path_to_binary
import os

class VillageCulturalProfileSerializer(serializers.ModelSerializer):
    religios_beliefs_image = serializers.SerializerMethodField()
    traditional_food_image = serializers.SerializerMethodField()
    traditional_dress_image = serializers.SerializerMethodField()
    traditional_ornaments_image = serializers.SerializerMethodField()
    festivals_image = serializers.SerializerMethodField()
    art_forms_practiced_image = serializers.SerializerMethodField()

    class Meta:
        model = VillageCulturalProfile
        fields = '__all__'

    def get_religios_beliefs_image(self, obj):
        return self._get_image_binaries(obj.religios_beliefs_image)

    def get_traditional_food_image(self, obj):
        return self._get_image_binaries(obj.traditional_food_image)

    def get_traditional_dress_image(self, obj):
        return self._get_image_binaries(obj.traditional_dress_image)

    def get_traditional_ornaments_image(self, obj):
        return self._get_image_binaries(obj.traditional_ornaments_image)

    def get_festivals_image(self, obj):
        return self._get_image_binaries(obj.festivals_image)

    def get_art_forms_practiced_image(self, obj):
        return self._get_image_binaries(obj.art_forms_practiced_image)

    def _get_image_binaries(self, image_list):
        """
        Convert image file paths to base64 binary format using utility function.
        Avoids duplicate prefixes if already included.
        """
        if not image_list:
            return []

        return [image_path_to_binary(img_path) for img_path in image_list]
