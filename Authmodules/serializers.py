from rest_framework import serializers
from .models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username","password","email")
    
class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username","password")