from rest_framework import serializers
from .models import Products


class ProductFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = "__all__"


class ReusableLockerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ("id","Views","Rating",'x','Image')
        non_updateable_fields = ("Views","Rating")
    def get_fields(self):
        fields = super().get_fields()
        specific_fields = getattr(self.Meta,'non_updateable_fields',())
        for f in fields:
            if self.instance and getattr(self.instance,f'{f}') is not None:
                if f in specific_fields:
                   fields[f'{f}'].read_only = True
        return fields