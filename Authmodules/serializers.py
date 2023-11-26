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

class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("password",)

class ForgotPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ("email",)