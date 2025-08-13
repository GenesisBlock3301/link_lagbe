import logging

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.auth_serializer import AuthenticationSerializer, UserSignupSerializer
from apps.users.docs import swagger_login, swagger_register

logger = logging.getLogger(__name__)


class UserSignupAPIView(APIView):
    serializer_class = UserSignupSerializer

    @swagger_register
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            return Response({
                'message': 'Account created successfully',
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response({
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationSerializer

    @swagger_login
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
