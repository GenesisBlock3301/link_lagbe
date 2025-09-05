import logging

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers.auth_serializer import AuthenticationSerializer, UserSignupSerializer, UserMeSerializer
from apps.users.docs import swagger_login, swagger_register, swagger_me
from apps.users.models import User
from apps.common.views import BaseAPIView as APIView

logger = logging.getLogger(__name__)


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignupSerializer

    @swagger_register
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    @swagger_login
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_me
    def get(self, request):
        user = (
            User.objects
            .select_related("profile")
            .prefetch_related("links")
            .get(pk=request.user.pk)
        )
        serializer = UserMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmailAPIView(APIView):
    def get(self, request, uidb64, token):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
