from rest_framework import serializers
from .models import Vendors

class VendorCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendors
        fields = ('Name','Address_line','City','State','Pin_code','Contact_no','Shop_icon')
    