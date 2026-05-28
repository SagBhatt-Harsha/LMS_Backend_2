from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (PlacementDashboardView, PlacementCandidateListView, InterviewViewSet, RetentionViewSet)

router = DefaultRouter()

router.register('interviews', InterviewViewSet, basename='interview')
router.register('retention', RetentionViewSet, basename='retention')

urlpatterns = [
    path('candidates/', PlacementCandidateListView.as_view()),
    path('', include(router.urls)),
]