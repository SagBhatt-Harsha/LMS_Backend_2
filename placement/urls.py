from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PlacementDashboardView, PlacementCandidateListView, InterviewViewSet, RetentionViewSet, RetentionRecordListView

router = DefaultRouter()

router.register('interviews', InterviewViewSet, basename='interview')
router.register('retention', RetentionViewSet, basename='retention')

urlpatterns = [
    path('candidates/', PlacementCandidateListView.as_view()),
    path('retention-records/', RetentionRecordListView.as_view()),
    path('dashboard/', PlacementDashboardView.as_view()),
    path('', include(router.urls)),
]