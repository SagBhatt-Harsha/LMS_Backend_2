from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ModuleViewSet, AssessmentViewSet, TrainerDashboardView, AdminTrainerDashboardView

router = DefaultRouter()

router.register('modules', ModuleViewSet, basename='module')
router.register('assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', TrainerDashboardView.as_view()),
    path('admin-dashboard/', AdminTrainerDashboardView.as_view()),
]