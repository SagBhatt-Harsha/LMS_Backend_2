from django.db.models import Count, Avg

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Assessment, Module, InternalAssessment, PerformanceCriteria
from .serializers import AssessmentSerializer, ModuleSerializer, InternalAssessmentSerializer, PerformanceCriteriaSerializer

from onboarding.models import Trainee
from batches.models import Batch
from teachers.models import Teacher
from .permissions import IsAdminCounsellorTeacher, IsTeacherOnly, IsAdminOnly

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = Module.objects.all()

        batch_id = self.request.query_params.get('batch_id')
        # GET /trainer/modules/?batch_id=
        if batch_id:
            queryset = queryset.filter(batch=batch_id)
        
         # Restrict teacher view:Logged-in Teacher can only view Modules for Batches Assigned to him/her.
        if getattr(self.request.user, 'role', None) == 'teacher':
            try:
                teacher = Teacher.objects.get(email=self.request.user.email)
                queryset = queryset.filter(batch__teacher=teacher)

            except Teacher.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        # So, that logged-in teacher cannot POST modules data if he/she is not associated with a Batch of the module's Domain.
        batch = serializer.validated_data['batch']

        try:
            teacher = Teacher.objects.get(email=self.request.user.email)

        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        serializer.save()

    def perform_update(self, serializer):
        # For PUT/PATCH: Logged-in teacher can't update modules for batches not assigned to him/her.
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        module = self.get_object()

        if module.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        serializer.save()

    def perform_destroy(self, instance):
        # For DELETE.
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        if instance.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        instance.delete()

class InternalAssessmentViewSet(viewsets.ModelViewSet):
    queryset = InternalAssessment.objects.all()
    serializer_class = InternalAssessmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOnly()]
        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = InternalAssessment.objects.all()
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            queryset = queryset.filter(batch=batch_id)
        
        if getattr(self.request.user, 'role', None) == 'teacher':
            try:
                teacher = Teacher.objects.get(email=self.request.user.email)
                queryset = queryset.filter(batch__teacher=teacher)
            except Teacher.DoesNotExist:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        batch = serializer.validated_data['batch']
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        serializer.save()

    def perform_update(self, serializer):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        assessment = self.get_object()
        if assessment.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        serializer.save()

    def perform_destroy(self, instance):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        if instance.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        instance.delete()

class PerformanceCriteriaViewSet(viewsets.ModelViewSet):
    queryset = PerformanceCriteria.objects.all()
    serializer_class = PerformanceCriteriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOnly()]
        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = PerformanceCriteria.objects.all()
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            queryset = queryset.filter(batch=batch_id)
        
        if getattr(self.request.user, 'role', None) == 'teacher':
            try:
                teacher = Teacher.objects.get(email=self.request.user.email)
                queryset = queryset.filter(batch__teacher=teacher)
            except Teacher.DoesNotExist:
                queryset = queryset.none()
        return queryset

    def perform_create(self, serializer):
        batch = serializer.validated_data['batch']
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        serializer.save()

    def perform_update(self, serializer):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        criteria = self.get_object()
        if criteria.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        serializer.save()

    def perform_destroy(self, instance):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")
        if instance.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")
        instance.delete()

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = Assessment.objects.all()

        batch_id = self.request.query_params.get('batch_id')
        trainee_id = self.request.query_params.get('trainee_id')

        if batch_id:
            queryset = queryset.filter(batch=batch_id)

        if trainee_id:
            queryset = queryset.filter(trainee=trainee_id)

         # Restrict Teacher View
        if getattr(self.request.user, 'role', None) == 'teacher':
            try:
                teacher = Teacher.objects.get(email=self.request.user.email)
                queryset = queryset.filter(batch__teacher=teacher)

            except Teacher.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def perform_create(self, serializer):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)

        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        batch = serializer.validated_data['batch']
        trainee = serializer.validated_data['trainee']

        if batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        if trainee.batch != batch:
            raise ValidationError("Trainee does not belong to this batch.")

        serializer.save(teacher=teacher)

    def perform_update(self, serializer):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        assessment = self.get_object()

        if assessment.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        # Prevent changing batch
        if ('batch' in serializer.validated_data and serializer.validated_data['batch'] != assessment.batch):
            raise ValidationError({
                "batch":"Batch cannot be changed."
            })

        # Prevent changing trainee
        if ('trainee' in serializer.validated_data and serializer.validated_data['trainee'] != assessment.trainee):
            raise ValidationError({
                "trainee":"Trainee cannot be changed."
            })

        serializer.save()

    def perform_destroy(self, instance):
        try:
            teacher = Teacher.objects.get(email=self.request.user.email)
        except Teacher.DoesNotExist:
            raise ValidationError("No teacher profile linked.")

        if instance.batch.teacher != teacher:
            raise ValidationError("You are not assigned to this batch.")

        instance.delete()

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
        trainees = Trainee.objects.filter(batches__in=trainer_batches).distinct()

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

        average_score = ( Assessment.objects.filter( batch__in=trainer_batches ).aggregate( avg = Avg('total_score') )['avg'] or 0 )

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
            "completion_ratio":completion_ratio,
            "average_score":round(average_score, 2)
        })


class AdminTrainerDashboardView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        total_batches = Batch.objects.count()
        trainees = Trainee.objects.all()

        completed_training = trainees.filter(training_completed=True).count()

        average_score = ( Assessment.objects.aggregate( avg = Avg('total_score') )['avg'] or 0 )

        # Domain-wise Completion Ratio
        domain_completion_rates = []

        domains = Batch.objects.values_list('domain', flat=True).distinct()

        for domain in domains:
            domain_trainees = Trainee.objects.filter(domain=domain)
            total_domain_students = domain_trainees.count()
            completed_domain_students = (domain_trainees.filter(training_completed=True).count())

            if total_domain_students > 0:
                completion_rate = round(completed_domain_students * 100 / total_domain_students, 2)

            else:
                completion_rate = 0

            domain_completion_rates.append({
                "domain": domain,
                "total_students": total_domain_students,
                "completed_students": completed_domain_students,
                "completion_rate": completion_rate
            })

        # Batch-wise Completion Ratio
        batch_completion_rates = []
        batches = Batch.objects.all()

        for batch in batches:
            batch_trainees = batch.trainees.all()
            total_batch_students = (batch_trainees.count())
            completed_batch_students = (batch_trainees.filter(training_completed=True).count())

            if total_batch_students > 0:
                completion_rate = round(completed_batch_students * 100 / total_batch_students, 2)
            else:
                completion_rate = 0

            batch_completion_rates.append({
                "batch_id": batch.id,
                "batch_name": batch.name,
                "total_students": total_batch_students,
                "completed_students": completed_batch_students,
                "completion_rate": completion_rate
            })

        return Response({
            "total_batches":total_batches,
            "students_enrolled":trainees.count(),
            "completed_training":completed_training,
            "average_score":round(average_score, 2),

            "domain_completion_rates":domain_completion_rates,
            "batch_completion_rates": batch_completion_rates
        })
