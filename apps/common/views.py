import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

from apps.common.exceptions import UserAlreadyExists, InvalidToken, PermissionDenied

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):

    exception_map = {
        UserAlreadyExists: {"message": "This email is already registered", "status": status.HTTP_400_BAD_REQUEST},
        InvalidToken: {"message": "Your token is invalid", "status": status.HTTP_401_UNAUTHORIZED},
        PermissionDenied: {"message": "Permission denied", "status": status.HTTP_403_FORBIDDEN},
    }

    def handle_exception(self, exc):
        if any(isinstance(exc, t) for t in self.exception_map):
            logger.error(f"{exc.__class__.__name__}: {exc}")
        else:
            logger.exception(f"Unexpected error in {self.__class__.__name__}: {exc}")

        if isinstance(exc, serializers.ValidationError):
            return Response({
                "message": "Validation failed",
                "errors": exc.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        for exc_type, info in self.exception_map.items():
            if isinstance(exc, exc_type):
                return Response({
                    "message": info["message"],
                    'status': info["status"] if "status" in info else status.HTTP_400_BAD_REQUEST,
                }, status=info["status"])

        return Response({
            "message": "An unexpected error occurred",
            "errors": str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
