import random
import logging

from celery.exceptions import CeleryError

from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.common.views import BaseAPIView as APIView
from apps.users.serializers import SendOtpSerializer, VerifyOTPSerializer, ResetPasswordSerializer
from apps.users.tasks import send_otp_email
from apps.users.docs import swagger_verify_otp, swagger_reset_password, swagger_send_otp


logger = logging.getLogger(__name__)
User = get_user_model()


class SendOtpAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SendOtpSerializer

    @swagger_send_otp
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if not user:
            logger.warning(f"OTP requested for non-existent email: {email}")
            return Response({"message": "If this email exists, OTP has been sent"}, status=status.HTTP_200_OK)


        # generate 4-digit otp
        otp = str(random.randint(1000, 9999))
        cache.set(f"forgot_password_otp:{user.email}", otp, timeout=300)

        # Send OTP asynchronously but handle possible Celery failure
        try:
            send_otp_email.delay(user.email, otp)
            logger.info(f"Successfully sent OTP email to {user.email}")
            print(otp)
            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        except CeleryError as e:
            logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")
            return Response(
                {"message": "Failed to send OTP. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyOTPAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    @swagger_verify_otp
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        stored_otp = cache.get(f"forgot_password_otp:{email}")
        if stored_otp != otp:
            return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    @swagger_reset_password
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        stored_otp = cache.get(f"forgot_password_otp:{email}")
        if stored_otp != otp:
            return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # Delete OTP from Redis after successful reset
        cache.delete(f"forgot_password_otp:{email}")

        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
