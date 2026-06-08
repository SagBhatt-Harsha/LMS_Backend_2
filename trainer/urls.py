from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ModuleViewSet, AssessmentViewSet, InternalAssessmentViewSet, PerformanceCriteriaViewSet, TrainerDashboardView, AdminTrainerDashboardView, TraineeGlobalAssessmentViewSet

router = DefaultRouter()

router.register('modules', ModuleViewSet, basename='module')
router.register('assessments', AssessmentViewSet, basename='assessment')
router.register('internal-assessments', InternalAssessmentViewSet, basename='internal-assessment')
router.register('performance-criteria', PerformanceCriteriaViewSet, basename='performance-criteria')
router.register('global-assessments', TraineeGlobalAssessmentViewSet, basename='global-assessment')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', TrainerDashboardView.as_view()),
    path('admin-dashboard/', AdminTrainerDashboardView.as_view()),
]