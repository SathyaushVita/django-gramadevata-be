
from rest_framework import serializers
from ..models import *
from datetime import datetime
from django.utils.timesince import timesince
# from .temple_serializers import TempleSerializer
from ..utils import *
from django.utils import timezone



class CommentSerializer(serializers.ModelSerializer): 
    posted_time_ago = serializers.SerializerMethodField()

    class Meta:
        model = CommentModel
        fields = '__all__'

    # def get_posted_time_ago(self,obj):
    #     return f"{timesince(obj.created_at)} ago"

    def get_posted_time_ago(self, obj):
        return f"{timesince(obj.created_at, timezone.now())} ago"       

class CommentSerializer12(serializers.ModelSerializer):


    user = serializers.SerializerMethodField(read_only=True)
    goshala = serializers.SerializerMethodField(read_only=True)
    event = serializers.SerializerMethodField(read_only=True)
    temple = serializers.SerializerMethodField(read_only=True)


    def get_temple(self, instance):
        user_i = instance.temple
        if user_i:
            print(user_i,"user_iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
            return {
                "name":user_i.name,
                "id":user_i._id,
               
            }

    
    
    def get_user(self, instance):
        user_i = instance.user
        if user_i:
            
            return {
                "name":user_i.full_name,
                "id":user_i.id,
                "username":user_i.username,
            #    "profile_pic":image_path_to_binary(instance.user.profile_pic)
            }
        
    def get_goshala(self, instance):

        goshala_i = instance.goshala
        if goshala_i:
            
            return {
                "name":goshala_i.name,
                "id":goshala_i._id,
                # "username":user_i.username
            }
        
    def get_event(self, instance):
            
        event_i = instance.event
        if event_i:
            
            return {
                "name":event_i.name,
                "id":event_i._id,
                # "username":user_i.username
            }




    class Meta:
        model = CommentModel
        fields = "__all__"

    def get_posted_time_ago(self,obj):
        return f"{timesince(obj.created_at)} ago"






