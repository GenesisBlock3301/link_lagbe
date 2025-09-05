from drf_yasg import openapi
from rest_framework import status


LoginRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, default="admin@yopmail.com"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, default="admin"),
    },
    required=["email", "password"]
)

LoginResponseSchema = openapi.Response(description="Login successful!")

RegisterRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, default="user@yopmail.com"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, default="123456"),
    },
    required=["email", "password"]
)

RegisterResponseSchema = openapi.Response(description="User created successfully!")


ProfileSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
        'gender': openapi.Schema(type=openapi.TYPE_STRING),
    }
)

UserMeSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "email": openapi.Schema(type=openapi.TYPE_STRING),
        "is_premium": openapi.Schema(type=openapi.TYPE_BOOLEAN),
        "profile": ProfileSchema,
    }
)

UserMeResponseSchema = {
    status.HTTP_200_OK: openapi.Response(
        description="Get User info successfully",
        schema=UserMeSchema
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Failed to get user info",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING, example="Get User info failed!")}
        )
    ),
    status.HTTP_401_UNAUTHORIZED: openapi.Response(
        description="Unauthorized",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"message": openapi.Schema(type=openapi.TYPE_STRING, example="You are not authorized to access this resource")}
        )
    ),
}
