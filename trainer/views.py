from django.db.models import Count

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Assessment
from .serializers import AssessmentSerializer

from onboarding.models import Trainee
from batches.models import Batch
from teachers.models import Teacher
from .permissions import IsAdminCounsellorTeacher,IsTeacherOnly

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOnly()]
        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = Assessment.objects.all()
        batch = self.request.query_params.get('batch')
        student = self.request.query_params.get('student')
        teacher = self.request.query_params.get('teacher')

        if batch:
            queryset = queryset.filter(batch=batch)

        if student:
            queryset = queryset.filter(trainee=student)

        if teacher:
            queryset = queryset.filter(teacher=teacher)

        return queryset

    def perform_create(self, serializer):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)

        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked with this account.")

        batch = serializer.validated_data['batch']

        # SECURITY CHECK

        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        serializer.save(teacher=teacher)
    
    def perform_create(self, serializer):

        try:
            teacher = Teacher.objects.get(email=self.request.user.email)

        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked with this account.")

        batch = serializer.validated_data['batch']

        # SECURITY CHECK
        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        serializer.save(teacher=teacher)

class TrainerDashboardView(APIView):
    permission_classes = [IsTeacherOnly]

    def get(self, request):
        # FIND LOGGED-IN TRAINER
        try:
            teacher = Teacher.objects.get(email=request.user.email)

        except Teacher.DoesNotExist:
            return Response({ "error" : "No teacher profile linked with this account." }, status=404)

        # TRAINER BATCHES
        trainer_batches = Batch.objects.filter(teacher=teacher)

        # TRAINER TRAINEES
        trainees = Trainee.objects.filter(batch__in=trainer_batches)

        # Dashboard Metrics
        students_under_training = trainees.count()

        female_students = trainees.filter(gender__iexact='Female').count()
        male_students = trainees.filter(gender__iexact='Male').count()

        sc_st_students = trainees.filter(registration__caste__in=['SC', 'ST']).count()
        obc_students = trainees.filter(registration__caste__in=['OBC']).count()

        completed_training = trainees.filter(training_completed=True).count()

        received_ssc_certificate = trainees.filter(ssc_certificate_received=True).count()

        if students_under_training > 0:
            completion_ratio = round( (completed_training / students_under_training) * 100, 1)

        else:
            completion_ratio = 0

        return Response({
            "trainer_name":teacher.name,
            "domain":teacher.domain,

            "total_batches":trainer_batches.count(),

            "students_under_training":students_under_training,

            "female_students":female_students,
            "male_students":male_students,

            "sc_st_students":sc_st_students,
            "obc_students":obc_students,

            "completed_training":completed_training,
            "received_ssc_certificate":received_ssc_certificate,
            "completion_ratio":completion_ratio
        })