from django.urls import path
from .views import LoginAPIView


urlpatterns = [
    # path('activate/<uid64>/<token>/', activate, name='activate'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
]
