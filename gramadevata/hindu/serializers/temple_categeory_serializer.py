from rest_framework import serializers
from ..models import *
from .temple_serializers import TempleSerializer
from ..utils import image_path_to_binary
from django.core.mail import send_mail
import random
from django.conf import settings
import re
import string
import requests
import base64
import os


class TempleCategeorySerializer1(serializers.ModelSerializer):
     class Meta:
          model = TempleCategory
          fields = ["_id","name"]


class TempleCategeorySerializer(serializers.ModelSerializer):
    
    
    pic = serializers.SerializerMethodField()

    def get_pic(self, instance):

            filename = instance.pic
            if filename:
                format= image_path_to_binary(filename)
                
                return format
            return None

    class Meta:
        model = TempleCategory
        fields = "__all__"




