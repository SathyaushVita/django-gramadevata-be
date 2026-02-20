


from rest_framework import serializers
from ..models import VillageDevelopmentFacility
from ..utils import image_path_to_binary  

class VillageDevelopmentFacilitySerializer(serializers.ModelSerializer):
    primarysource_of_livelihood_image = serializers.SerializerMethodField()

    class Meta:
        model = VillageDevelopmentFacility
        fields = '__all__'

    def get_primarysource_of_livelihood_image(self, obj):
        images = obj.primarysource_of_livelihood_image or []
        return [image_path_to_binary(img) for img in images]

