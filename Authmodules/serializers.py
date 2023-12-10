from rest_framework import serializers
from rest_framework.fields import empty
from .models import CustomUser,Address

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

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ("id","user")


class AccountInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username","Profile_pic","Petal_credits","Phone_no","email","id")
        extra_kwargs = {
            "email":{"read_only":True},
            "Petal_credits":{"read_only":True},
        }
    
