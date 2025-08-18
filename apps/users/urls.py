from django.urls import path
from .views import (LoginAPIView, SignupAPIView, VerifyEmailAPIView, SendOtpAPIView, ResetPasswordAPIView,
                    VerifyOTPAPIView)

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailAPIView.as_view(), name='verify-email'),
]

password_urlpatterns = [
    path('send-otp/', SendOtpAPIView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
]

urlpatterns += password_urlpatterns
