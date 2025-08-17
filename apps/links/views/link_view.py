from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from apps.common.views import BaseAPIView as APIView
from apps.links.models import Link
from apps.links.serializers import LinkSerializer
from apps.links.docs import (swagger_link_retrieve_response, swagger_link_list_response, swagger_link_create_response,
                             swagger_link_update_response, swagger_link_delete_response)


class LinkListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LinkSerializer

    @swagger_link_list_response
    def get(self, request):
        queryset = Link.objects.filter(user=request.user)
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
