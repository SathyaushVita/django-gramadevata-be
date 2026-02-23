
from rest_framework import serializers
from ..models import Register

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


    class Meta:
        model = Register
        fields = ["email","password"]