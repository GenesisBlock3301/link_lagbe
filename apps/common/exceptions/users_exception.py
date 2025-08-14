from rest_framework import status

from .base_exception import  BaseAPIException


class UserAlreadyExists(BaseAPIException):
    default_detail = "A user with this email already exists."
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidToken(BaseAPIException):
    default_detail = "Token is invalid or expired."
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseAPIException):
    default_detail = "You do not have permission to perform this action."
    status_code = status.HTTP_403_FORBIDDEN
