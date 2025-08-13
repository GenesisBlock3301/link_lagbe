from drf_yasg import openapi


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
