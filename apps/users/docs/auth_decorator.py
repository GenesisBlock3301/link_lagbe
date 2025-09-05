from drf_yasg.utils import swagger_auto_schema
from .auth_schema import (RegisterResponseSchema, LoginResponseSchema, LoginRequestSchema, RegisterRequestSchema,
                          UserMeResponseSchema)
from rest_framework import status


def swagger_login(func):
    return swagger_auto_schema(
        tags=['Users'],
        request_body=LoginRequestSchema,
        responses={status.HTTP_201_CREATED: LoginResponseSchema}
    )(func)


def swagger_register(func):
    return swagger_auto_schema(
        tags=['Users'],
        request_body=RegisterRequestSchema,
        responses={status.HTTP_201_CREATED: RegisterResponseSchema}
    )(func)


def swagger_me(func):
    return swagger_auto_schema(
        tags=['Users'],
        responses=UserMeResponseSchema
    )(func)
