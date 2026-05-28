from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (AssessmentViewSet, TrainerDashboardView)

router = DefaultRouter()

router.register('assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('',include(router.urls)),
]