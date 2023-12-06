import time
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from django.utils.decorators import method_decorator
from .models import CustomUser,Address
from .serializers import SignUpSerializer,LoginSerializer,ResetPasswordSerializer,ForgotPasswordSerializer,AccountInformationSerializer,AddressSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all() 

    def post(self,request,*args, **kwargs):
         if CustomUser.objects.filter(username = request.data.get('username')).exists() or CustomUser.objects.filter(email = request.data.get('email')).exists():
              return Response({"message":"Credentials already exists"},status = status.HTTP_400_BAD_REQUEST)
         else:
              serializer = SignUpSerializer(data = request.data)
              serializer.is_valid(raise_exception=True)
              serializer.save()
              user = serializer.instance
              user.Verified = False
              try:
                token,_ = Token.objects.get_or_create(user = user)
              except:
                   user.delete()
                   return Response({'message':'unable to create account:Token authentication failed'},status = status.HTTP_400_BAD_REQUEST)
              subject = 'Verification mail'
              message = f'Verify here -> http://adhishraya.pythonanywhere.com/accounts/verify?id={user.id}'
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [user.email,]
              send_mail(subject,message,email_from,recipient_list)
              return Response({'message':'Account Created!, Verify account through mail','user_id':user.id},status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt,name= 'get')             
class EmailVerificationView(APIView):
     permission_classes = (AllowAny,)

     def get(self,request):
          id = self.request.query_params.get('id')
          user = CustomUser.objects.get(id = id)
          user.Verified = True
          user.save()
          return Response({"message":"Email verified"},status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
     permission_classes = (AllowAny,)
     serializer_class  = LoginSerializer
     queryset = CustomUser.objects.all()

     def post(self,request,*args, **kwargs):
         try:
            user = CustomUser.objects.get(username = request.data.get('username'))
            if user.password == request.data.get('password') and user.Verified == True:
              login(request,user)
              token,_ = Token.objects.get_or_create(user = user)
              user_data = AccountInformationSerializer(user)
              return Response({"message":"Succesful login","token":token.key,"user_id":user.id,"user_data":user_data.data},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Please use correct credentials"},status=status.HTTP_400_BAD_REQUEST)
         except:
              return Response({'message','User doesnt exist'},status=status.HTTP_400_BAD_REQUEST)
         

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def get(self,request):
          user = self.request.user
          token = Token.objects.get(user = user)
          logout(request)
          token.delete()
          return Response({"message":"Succesfully logged out"},status=status.HTTP_200_OK)
     
@method_decorator(csrf_exempt,name = 'post')
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer
    def post(self,request,*args, **kwargs):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email = email)
            subject = 'Password reset mail'
            message = f'Reset password here -> http://adhishraya.pythonanywhere.com/accounts/resetpassword?id={user.id}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject,message,email_from,recipient_list)
            return Response({"message":"password reset mail sent succesfully"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"No account with this mail found"},status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt,name = 'post')
class ResetPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        user = CustomUser.objects.get(id = user_id)
        password = request.data.get('password')
        user.password = password
        user.save()
        return Response({"message":"Password reset succesfull"},status=status.HTTP_200_OK)

@method_decorator(csrf_exempt,name = 'post')
class ResetEmailView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        user = CustomUser.objects.get(id = user_id)
        user.email = request.data.get('email')
        user.save()
        return Response({"message":"Email reset succesfull"},status=status.HTTP_200_OK)


class EditAccountMailView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        try:
           user = CustomUser.objects.get(id = user_id)
           subject = 'mail reset'
           message =  message = f'Reset mail here -> http://adhishraya.pythonanywhere.com/accounts/resetmail?id={user.id}'
           email_from = settings.EMAIL_HOST_USER
           recipient_list = [user.email,]
           send_mail(subject,message,email_from,recipient_list)
           return Response({"message":"Email reset link has been sent to your account mail"})
        except:
           return Response({"message":"An error occured"},status=status.HTTP_200_OK)
      

class GetAccountInfoView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountInformationSerializer
    def get(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        try:
          user = CustomUser.objects.get(id = user_id)
          serializer = AccountInformationSerializer(user)
          addresses = Address.objects.filter(user = user)
          data = []
          data.append(serializer.data)
          address_serializer = AddressSerializer(addresses,many = True)
          data.append(address_serializer.data)
          return Response({"data":data},status=status.HTTP_200_OK)
        except:
            return Response({"message":"An error occured"},status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        user_id = self.request.query_params.get('id')
        user = CustomUser.objects.get(id = user_id)
        data = request.data
        if data.get("Profile_pic"):
            user.Profile_pic = data.get("Profile_pic")
        if data.get("Petal_credits"):
            user.Petal_credits = data.get("Petal_credits")
        if data.get("Phone_no"):
            user.Phone_no = data.get("Phone_no")
        user.save()
        serializer = AccountInformationSerializer(user)
        addresses = Address.objects.filter(user = user)
        data = []
        data.append(serializer.data)
        address_serializer = AddressSerializer(addresses,many = True)
        data.append(address_serializer.data)
        return Response({"data":data},status=status.HTTP_200_OK)
       
class GetAddressView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer

    def get(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        try:
          user = CustomUser.objects.get(id = user_id)
          Addresses = Address.objects.filter(user = user)
          return Response({"data":Addresses},status=status.HTTP_200_OK)
        except:
            return Response({"message":"An error occured"},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,*args, **kwargs):
        user_id = self.request.query_params.get('id')
        user = CustomUser.objects.get(id = user_id)
        serializer = AddressSerializer(data = request.data)
        serializer.is_valid()
        serializer.save()
        address = serializer.instance
        address.user = user
        address.save()
        addresses = Address.objects.filter(user = user)
        serializer2 = AddressSerializer(addresses,many = True)
        return Response({
                "message":"Address added succesfully",
                "data":serializer2.data
        },status=status.HTTP_201_CREATED)
    
class AddAddressview(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddressSerializer
    def post(self,request,*args, **kwargs):
        user = self.request.user
        request.data['user']  = user
        serializer = AddressSerializer(request.data)
        serializer.save()
        return Response({"message":"Address saved"},status=status.HTTP_200_OK)