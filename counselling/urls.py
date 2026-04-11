from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CounsellingViewSet

router = DefaultRouter()

router.register('', CounsellingViewSet, basename='counselling')

urlpatterns = [
    path('',include(router.urls)),
]