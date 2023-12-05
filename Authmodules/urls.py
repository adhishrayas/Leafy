from django.urls import path
from .views import SignUpView,EmailVerificationView,LoginView,LogoutView,ForgotPasswordView,ResetPasswordView,EditAccountMailView,GetAccountInfoView,GetAddressView


app_name = 'Authmodules'
urlpatterns = [
    path('signup',SignUpView.as_view(),name = "signup"),
    path('verify',EmailVerificationView.as_view(),name = "Verify"),
    path('login',LoginView.as_view(),name = "login"),
    path('logout',LogoutView.as_view(),name = "logout"),
    path('forgotpassword',ForgotPasswordView.as_view(),name = "Forgot Password"),
    path('resetpassword',ResetPasswordView.as_view(),name = "Reset Password"),
    path('editmail',EditAccountMailView.as_view(),name = 'Edit Account Mail'),
    path('editAccount',GetAccountInfoView.as_view(),name = "Account info"),
    path('editAddress',GetAddressView.as_view(),name = 'Address edit'),
]


