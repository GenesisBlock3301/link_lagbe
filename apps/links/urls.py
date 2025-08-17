from django.urls import path
from apps.links.views import (
    LinkListAPIView,
    LinkCreateAPIView,
    LinkRetrieveAPIView,
    LinkUpdateAPIView,
    LinkDeleteAPIView
)

urlpatterns = [
    path('', LinkListAPIView.as_view(), name='link-list'),
    path('create/', LinkCreateAPIView.as_view(), name='link-create'),
    path('<int:pk>/', LinkRetrieveAPIView.as_view(), name='link-retrieve'),
    path('<int:pk>/update/', LinkUpdateAPIView.as_view(), name='link-update'),
    path('<int:pk>/delete/', LinkDeleteAPIView.as_view(), name='link-delete'),
]
