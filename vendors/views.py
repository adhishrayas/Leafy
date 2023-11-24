from django.shortcuts import render
from helpers.permissions import is_already_buyer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView,CreateAPIView
from .serializers import VendorCreationSerializer
# Create your views here.

class CreateVendorView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VendorCreationSerializer
