from rest_framework import serializers
from ..models import ConnectModel
from .member_serializer import MemberSerializer
from ..utils import image_path_to_binary
from django.conf import settings

class ConnectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectModel
        fields = "__all__"


class ConnectModelSerializer1(serializers.ModelSerializer):
    village = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    temple = serializers.SerializerMethodField()
    
    def get_image_location(self, temple):
        filename = temple.image_location
        if filename:
            # Handle cases where filename is a list
            if isinstance(filename, list):
                # Use the first item in the list as the filename
                filename = filename[0]
            # Ensure the filename is a string before proceeding
            if isinstance(filename, str):
                # Check for JSON-like format
                if filename.startswith('[') and filename.endswith(']'):
                    # Remove brackets and quotes, then split by comma
                    filename = filename.strip('[]').replace('"', '').split(',')[0].strip()
                # Replace slashes to match desired format
                formatted_filename = filename.replace("/", "\\").replace("\\\\", "\\")
                return f"{settings.FILE_URL}{formatted_filename}"
        return None

    def get_village(self, instance):
        village = instance.village
        if village:
            return {
                "_id": str(village._id),
                "name": village.name,
                "image_location": self.get_image_location(village)
            }

    def get_user(self, instance):
        user = instance.user
        if user:
            return {
                "_id": user.id,
                "name": user.full_name,
                "father_name": user.father_name,
                "contact_number": user.contact_number,
                "dob": user.dob,
                "type": user.type,
                "username": user.username,
                'account_type':user.account_type
            }

    def get_temple(self, instance):
        temple = instance.temple
        if temple:
            return {
                "_id": str(temple._id),
                "name": temple.name,
                "image_location": self.get_image_location(temple),  # Use self here
            }
        return None

    class Meta:
        model = ConnectModel
        fields = '__all__'








