from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import ProductFeedSerializer,ReusableLockerSerializer
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from Authmodules.models import CustomUser,Address
from .models import Products
# Create your views here.

class ProductFeedView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductFeedSerializer
    def get(self,request,*args, **kwargs):
        prod = Products.objects.all().first()
        serializer = ProductFeedSerializer(prod)
        data = []
        data.append(serializer.data)
        return Response({'data':data},status = status.HTTP_200_OK)
    
class ProductDetailView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReusableLockerSerializer
    queryset = Products.objects.all()

