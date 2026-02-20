

from rest_framework import serializers
from ..models import GoshalaCategory
from ..utils import image_path_to_binary

class GoshalaCategorySerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    def get_pic(self, instance):

            filename = instance.pic
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None



    class Meta:
        model = GoshalaCategory
        fields = ('_id', 'name', 'desc', 'created_at', 'pic')