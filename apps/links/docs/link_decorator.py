from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .link_schema import (
    LinkListResponseSchema,
    LinkCreateRequestSchema,
    LinkCreateResponseSchema,
    LinkRetrieveResponseSchema,
    LinkUpdateRequestSchema,
    LinkUpdateResponseSchema,
    LinkDeleteResponseSchema,
    LinkOrderUpdateResponseSchema,
    LinkOrderUpdateResponseSchema
)

# ---------------- List ----------------
def swagger_link_list_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        responses={status.HTTP_200_OK: LinkListResponseSchema}
    )(func)


# ---------------- Create ----------------
def swagger_link_create_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        request_body=LinkCreateRequestSchema,
        responses={status.HTTP_201_CREATED: LinkCreateResponseSchema}
    )(func)


# ---------------- Retrieve ----------------
def swagger_link_retrieve_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        responses={status.HTTP_200_OK: LinkRetrieveResponseSchema}
    )(func)


# ---------------- Update (PUT) ----------------
def swagger_link_update_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        request_body=LinkUpdateRequestSchema,
        responses={status.HTTP_200_OK: LinkUpdateResponseSchema}
    )(func)


# ---------------- Delete ----------------
def swagger_link_delete_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        responses={status.HTTP_204_NO_CONTENT: LinkDeleteResponseSchema}
    )(func)


def swagger_link_order_response(func):
    return swagger_auto_schema(
        tags=['Links'],
        request_body=LinkCreateRequestSchema,
        responses=LinkOrderUpdateResponseSchema
    )(func)
