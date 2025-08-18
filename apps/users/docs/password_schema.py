from drf_yasg import openapi
from rest_framework import status

SendOtpRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="User email to send OTP"
        ),
    },
    required=["email"],
)

VerifyOtpRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
        "otp": openapi.Schema(type=openapi.TYPE_STRING, description="OTP received in email"),
    },
    required=["email", "otp"],
)

ResetPasswordRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING),
        "otp": openapi.Schema(type=openapi.TYPE_STRING),
        "new_password": openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=["email", "otp", "new_password"],
)


def response_schema(message: str):
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING, example=message)
        }
    )


SendOtpResponses = {
    status.HTTP_200_OK: openapi.Response(
        description="OTP sent successfully",
        schema=response_schema("OTP sent successfully")
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Failed to send OTP",
        schema=response_schema("Email does not exist or invalid")
    ),
    status.HTTP_404_NOT_FOUND: openapi.Response(
        description="OTP not found",
        schema=response_schema("OTP not found")
    )
}

VerifyOtpResponses = {
    status.HTTP_200_OK: openapi.Response(
        description="OTP verified successfully",
        schema=response_schema("OTP verified successfully")
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Invalid or expired OTP",
        schema=response_schema("Invalid or expired OTP")
    ),
    status.HTTP_404_NOT_FOUND: openapi.Response(
        description="OTP not found",
        schema=response_schema("OTP not found")
    )
}

ResetPasswordResponses = {
    status.HTTP_200_OK: openapi.Response(
        description="Password reset successfully",
        schema=response_schema("Password reset successfully")
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Invalid OTP or input",
        schema=response_schema("Invalid OTP or input")
    ),
    status.HTTP_404_NOT_FOUND: openapi.Response(
        description="OTP not found",
        schema=response_schema("OTP not found")
    )
}
