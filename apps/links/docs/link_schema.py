from drf_yasg import openapi
from rest_framework import status

LinkSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Link ID"),
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Link title"),
        "url": openapi.Schema(type=openapi.TYPE_STRING, description="Link URL"),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, description="Display order"),
        "click_count": openapi.Schema(type=openapi.TYPE_INTEGER, description="Number of clicks"),
        "created_at": openapi.Schema(type=openapi.FORMAT_DATETIME, description="Creation timestamp"),
    },
    required=["id", "title", "url"]
)

# Response schema for list of links
LinkListResponseSchema = openapi.Response(
    description="List of links",
    schema=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=LinkSchema
    )
)

# Link create request body
LinkCreateRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Link title", default="My Link"),
        "url": openapi.Schema(type=openapi.TYPE_STRING, description="Link URL", default="https://example.com"),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, description="Display order", default=0),
    },
    required=["title", "url"]
)

# Link Create Response
LinkCreateResponseSchema = openapi.Response(
    description="Link created successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Link ID"),
            "title": openapi.Schema(type=openapi.TYPE_STRING),
            "url": openapi.Schema(type=openapi.TYPE_STRING),
            "order": openapi.Schema(type=openapi.TYPE_INTEGER),
            "click_count": openapi.Schema(type=openapi.TYPE_INTEGER),
            "created_at": openapi.Schema(type=openapi.FORMAT_DATETIME),
        }
    )
)

# Link retrieve
LinkRetrieveResponseSchema = openapi.Response(
    description="Retrieve single link",
    schema=LinkSchema  # reuse LinkSchema defined before
)

# Link Update request body
LinkUpdateRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Link title"),
        "url": openapi.Schema(type=openapi.TYPE_STRING, description="Link URL"),
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, description="Display order"),
    },
    required=["title", "url"]
)

#  Link Update Response body
LinkUpdateResponseSchema = openapi.Response(
    description="Link updated successfully",
    schema=LinkSchema
)

# Delete Response Schema
LinkDeleteResponseSchema = openapi.Response(
    description="Link deleted successfully (soft delete)",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"detail": openapi.Schema(type=openapi.TYPE_STRING, default="Link deleted successfully")}
    )
)

LinkOrderUpdateRequestSchema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "order": openapi.Schema(type=openapi.TYPE_INTEGER, description="Display order"),
    }
)

LinkOrderUpdateResponseSchema = {
    status.HTTP_200_OK: openapi.Response(
        description="Link order updated successfully",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Message"),
            }
        )
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Link order update failed",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="Message"),
            }
        )
    )
}
