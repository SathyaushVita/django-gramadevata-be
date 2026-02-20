from rest_framework import serializers
from ..models import AddMoreVeterinaryHospital
from django.conf import settings

class AddMoreVeterinaryHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddMoreVeterinaryHospital
        fields = "__all__"
        extra_kwargs = {
            'image_location': {'required': False, 'default': list},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Format images with FILE_URL
        if instance.image_location:
            image_locations = (
                instance.image_location
                if isinstance(instance.image_location, list)
                else instance.image_location.strip('[]').replace('"', '').split(',')
            )
            representation['image_location'] = [f"{settings.FILE_URL}{path.strip()}" for path in image_locations]
        else:
            representation['image_location'] = []
        return representation
