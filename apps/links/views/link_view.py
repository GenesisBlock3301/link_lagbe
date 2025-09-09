import time

from django.db.models import Count
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from apps.common.views import BaseAPIView as APIView
from apps.links.models import Link
from apps.links.serializers import LinkSerializer
from apps.links.docs import (swagger_link_retrieve_response, swagger_link_list_response, swagger_link_create_response,
                             swagger_link_update_response, swagger_link_delete_response, swagger_link_order_response)


class LinkListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    @swagger_link_list_response
    def get(self, request):
        start = time.time()
        queryset = Link.objects.annotate(
            click_count=Count('clicks'),
        ).filter(user=request.user)
        end = time.time()
        print(end - start)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class LinkCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    @swagger_link_create_response
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


class LinkRetrieveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    def get_object(self, pk, user):
        obj = Link.objects.filter(pk=pk, user=user).first()
        if not obj:
            raise NotFound()
        return obj

    @swagger_link_retrieve_response
    def get(self, request, pk):
        link = self.get_object(pk, request.user)
        serializer = self.serializer_class(link)
        return Response(serializer.data)


class LinkUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    def get_object(self, pk, user):
        obj = Link.objects.filter(pk=pk, user=user).first()
        if not obj:
            raise NotFound()
        return obj

    @swagger_link_update_response
    def put(self, request, pk):
        link = self.get_object(pk, request.user)
        serializer = self.serializer_class(link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        raise ValidationError(serializer.errors)


class LinkDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    def get_object(self, pk, user):
        obj = Link.objects.filter(pk=pk, user=user).first()
        if not obj:
            raise NotFound()
        return obj

    @swagger_link_delete_response
    def delete(self, request, pk):
        link = self.get_object(pk, request.user)
        # Soft delete
        link.is_active = False
        link.is_deleted = True
        link.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkOrderUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_link_order_response
    def patch(self, request, pk):
        try:
            link = request.user.links.get(pk=pk)
        except Link.DoesNotExist:
            return Response({"error": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

        new_order = request.data.get("order")
        if new_order is None:
            return Response({"error": "Order field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_order = int(new_order)
        except ValueError:
            return Response({"error": "Order must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        link.order = new_order
        link.save(update_fields=["order"])
        return Response({"id": link.id, "order": link.order}, status=status.HTTP_200_OK)


class LinkToggleUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_link_update_response
    def patch(self, request, pk):
        try:
            link = request.user.links.get(pk=pk)
        except Link.DoesNotExist:
            return Response({"error": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

        link.is_active = not link.is_active
        link.save(update_fields=["is_active"])
        return Response({"id": link.id, "is_active": link.is_active}, status=status.HTTP_200_OK)
