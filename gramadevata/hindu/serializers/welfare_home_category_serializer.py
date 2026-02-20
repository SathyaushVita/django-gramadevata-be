from rest_framework import serializers
from ..models import WelfareHomesCategory
from ..utils import image_path_to_binary

class WelfareHomesCategorySerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return None

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Handle stringified list like "['path\\to\\image.jpg']"
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = WelfareHomesCategory
        fields = "__all__"





class WelfareHomesCategorySerializer(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location

        if not filename:
            return None

        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            # Handle stringified list like "['path\\to\\image.jpg']"
            filename = filename.strip('[]').replace('"', '').replace("'", '')
            image_paths = [path.strip() for path in filename.split(',') if path.strip()]
        else:
            image_paths = []

        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = WelfareHomesCategory
        fields = ["_id","name","image_location"]