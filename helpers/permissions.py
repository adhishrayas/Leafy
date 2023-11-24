from rest_framework import permissions,status
from rest_framework.response import Response


class is_already_buyer(permissions.BasePermission):
    
    def has_object_permission(self,request,view,obj):
        if obj.Type == 1:
            return Response({'message':'User is already a buyer'},status= status.HTTP_401_UNAUTHORIZED)
        return True
