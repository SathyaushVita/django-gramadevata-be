from rest_framework import serializers
from ..models import MemberModel

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        fields = "__all__"



class MemberSerializer1(serializers.ModelSerializer):
    village = serializers.SerializerMethodField()
       
        
    class Meta:
        model = MemberModel
        fields = "__all__"