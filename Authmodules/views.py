from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from django.utils.decorators import method_decorator
from .models import CustomUser
from .serializers import SignUpSerializer,LoginSerializer,ResetPasswordSerializer,ForgotPasswordSerializer
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
              try:
                token,_ = Token.objects.get_or_create(user = user)
              except:
                   user.delete()
                   return Response({'message':'unable to create account:Token authentication failed'},status = status.HTTP_400_BAD_REQUEST)
              login(request,user)
              return Response({'token':token.key,'data':serializer.data},status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt,name= 'get')             
class EmailVerificationView(APIView):
     permission_classes = (AllowAny,)

     def get(self,request):
          id = self.request.query_params.get('id')
          user = CustomUser.objects.get(id = id)
          user.Verified = True
          user.save()
          return Response({"message":"Email Verified"},status = status.HTTP_200_OK)


class LoginView(GenericAPIView):
     permission_classes = (AllowAny,)
     serializer_class  = LoginSerializer
     queryset = CustomUser.objects.all()

     def post(self,request,*args, **kwargs):
         try:
            user = CustomUser.objects.get(username = request.data.get('username'))
            if user.password == request.data.get('password'):
              login(request,user)
              token,_ = Token.objects.get_or_create(user = user)
              return Response({"message":"Succesful login","token":token.key},status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)
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
    