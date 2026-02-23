from rest_framework import serializers
from ..models import VillageFamousPersonality,Register
from ..utils import image_path_to_binary
from django.utils.timesince import timesince
from django.utils import timezone

class VillageFamousPersonalitySerializer(serializers.ModelSerializer):
    person_image=serializers.SerializerMethodField()
    def get_person_image(self, instance):
        filename = instance.person_image
        
        # Check if filename is a list or a string
        if isinstance(filename, list):
            # If it's already a list, return it as is
            image_paths = filename
        elif isinstance(filename, str):
            # If it's a string, attempt to parse it as a list-like string
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            # If it's neither a list nor a string, return an empty list
            image_paths = []

        # Apply binary conversion (assuming `image_path_to_binary` is defined)
        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = VillageFamousPersonality
        fields = '__all__'
        extra_kwargs = {'person_image': {'required': False, 'default': list}}





class InactiveVillageFamousPersonalitySerializer(serializers.ModelSerializer):
    person_image=serializers.SerializerMethodField()
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


    def get_person_image(self, instance):
        filename = instance.person_image
        
        if isinstance(filename, list):
            image_paths = filename
        elif isinstance(filename, str):
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            image_paths = []
        return [image_path_to_binary(path) for path in image_paths]

    class Meta:
        model = VillageFamousPersonality
        fields = '__all__'
        extra_kwargs = {'person_image': {'required': False, 'default': list}}
