from rest_framework import serializers
from ..models import TempleMainCategory
from ..utils import image_path_to_binary


class TempleMainCategorySerializer(serializers.ModelSerializer):
    
    
    pic = serializers.SerializerMethodField()

    def get_pic(self, instance):

            filename = instance.pic
            if filename:
                format= image_path_to_binary(filename)
                
                return format
            return None

    class Meta:
        model = TempleMainCategory
        fields = "__all__"
