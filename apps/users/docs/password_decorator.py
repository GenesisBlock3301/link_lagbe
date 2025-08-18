from drf_yasg.utils import swagger_auto_schema
from .password_schema import (
    SendOtpRequestSchema, SendOtpResponses,
    VerifyOtpRequestSchema, VerifyOtpResponses,
    ResetPasswordRequestSchema, ResetPasswordResponses,
)


def swagger_send_otp(func):
    return swagger_auto_schema(
        tags=['Users'],
        request_body=SendOtpRequestSchema,
        responses=SendOtpResponses
    )(func)


def swagger_verify_otp(func):
    return swagger_auto_schema(
        tags=['Users'],
        request_body=VerifyOtpRequestSchema,
        responses=VerifyOtpResponses
    )(func)


def swagger_reset_password(func):
    return swagger_auto_schema(
        tags=['Users'],
        request_body=ResetPasswordRequestSchema,
        responses=ResetPasswordResponses
    )(func)
