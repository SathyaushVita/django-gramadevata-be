from rest_framework import serializers
from ..models import ChatModel,Register
from django.utils.timesince import timesince



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = "__all__"


class ChatSerializer1(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
     

    def get_user(self, instance):
        try:
            user = instance.user  # This accesses the related Register object
            return {
                "_id": user.id,
                "name": user.full_name,
                "father_name": user.father_name,
                "contact_number": user.contact_number,
                "dob": user.dob,
                "type": user.type,
                "username": user.username
            }
        except Register.DoesNotExist:  # Handle missing user gracefully
            return None

    class Meta:
        model = ChatModel
        fields = "__all__"
        # You can also list fields explicitly if needed

    def get_posted_time_ago(self,obj):
        return f"{timesince(obj.created_at)} ago"
