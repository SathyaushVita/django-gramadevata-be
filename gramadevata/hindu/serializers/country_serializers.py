from rest_framework import serializers
from ..models import *
from ..utils import image_path_to_binary


class CountrySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Country
        fields = ["_id","name"]

class CountrySerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()
    def get_image_location(self, instance):

            filename = instance.image_location
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return[]

    class Meta:
        model = Country
        fields =  ["_id","name","image_location"]