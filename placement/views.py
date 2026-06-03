from django.db.models import Count
from django.db import transaction

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from onboarding.models import Trainee
from .models import Interview, Retention

from .serializers import (PlacementCandidateSerializer, InterviewSerializer, RetentionSerializer, RetentionMonthSerializer, RetentionRecordSerializer)
from .permissions import (IsPlacementOfficerOnly, IsAdminCounsellorPlacement, IsAdminOnly, IsAdminPlacement)

# Create your views here.
class PlacementDashboardView(APIView):
    permission_classes = [IsAdminCounsellorPlacement]

    def get(self, request):
        registered_for_training = Trainee.objects.count()

        appeared_for_interview = Interview.objects.filter(status='Appeared').values('trainee').distinct().count()
        students_placed = Interview.objects.filter(status='Selected').values('trainee').distinct().count()

        retained_6_months = Retention.objects.filter(month_number=6,retention_status__in=[
            'Retained', 'Changed']).values('trainee').distinct().count()

        completed_training = Trainee.objects.filter(training_completed=True).count()

        # RATIOS
        if registered_for_training > 0:
            training_completion_rate = round((completed_training / registered_for_training) * 100, 1)
        else:
            training_completion_rate = 0

        if completed_training > 0:
            interview_rate = round((appeared_for_interview / completed_training) * 100, 1)
        else:
            interview_rate = 0

        if appeared_for_interview > 0:
            placement_rate = round(( students_placed / appeared_for_interview) * 100, 1)
        else:
            placement_rate = 0

        if students_placed > 0:
            retention_rate_6_months = round((retained_6_months / students_placed) * 100, 1)
        else:
            retention_rate_6_months = 0

        # DOMAIN PLACEMENTS
        domain_placements = []

        for domain in Trainee.objects.values_list('domain', flat=True).distinct():
            total = Trainee.objects.filter(domain=domain).count()
            placed = Interview.objects.filter(trainee__domain=domain, status='Selected').values('trainee').distinct().count()

            percentage = 0

            if total > 0:
                percentage = round((placed / total) * 100, 1)

            domain_placements.append({"domain": domain,"placed_percentage": percentage})

    
        # DOMAIN RETENTION
        domain_retention = []

        for domain in Trainee.objects.values_list('domain', flat=True).distinct():
            placed = Interview.objects.filter(trainee__domain=domain, status='Selected').values('trainee').distinct().count()

            retained = Retention.objects.filter(
                trainee__domain=domain, month_number=6, retention_status__in=[
                    'Retained', 'Changed']).values('trainee').distinct().count()

            percentage = 0
            if placed > 0:
                percentage = round((retained / placed) * 100, 1)

            domain_retention.append( {"domain": domain, "retention_percentage": percentage} )

        return Response({

            "summary": {

                "registered_for_training":
                registered_for_training,

                "appeared_for_interview":
                appeared_for_interview,

                "students_placed":
                students_placed,

                "retained_6_months":
                retained_6_months
            },

            "ratios": {

                "training_completion_rate":
                training_completion_rate,

                "interview_rate":
                interview_rate,

                "placement_rate":
                placement_rate,

                "retention_rate_6_months":
                retention_rate_6_months
            },

            "domain_placements":
            domain_placements,

            "domain_retention":
            domain_retention
        })


class PlacementCandidateListView(ListAPIView):

    serializer_class = PlacementCandidateSerializer
    permission_classes = [IsAdminCounsellorPlacement]

    def get_queryset(self):
        queryset = Trainee.objects.filter(eligible_for_placement=True)
        domain = self.request.query_params.get('domain')
        gender = self.request.query_params.get('gender')
        eligibility = self.request.query_params.get('eligibility')

        if domain:
            queryset = queryset.filter(domain=domain)

        if gender:
            queryset = queryset.filter(gender=gender)

        if eligibility == 'completed_assessment':
            queryset = queryset.filter(training_completed=True)

        return queryset


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [IsAdminPlacement]

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_create(self, request):
        # POST /api/placement/interviews/bulk/
        trainee_id = request.data.get('trainee')
        interviews = request.data.get('interviews', [])

        if len(interviews) > 3:
            return Response(
                {
                    "error":"Maximum 3 interviews allowed."
                },
                status=400
            )

        try:
            trainee = Trainee.objects.get(id=trainee_id)

        except Trainee.DoesNotExist:
            return Response(
                {
                    "error":"Invalid trainee."
                },
                status=404
            )

        created = []
        with transaction.atomic():
            for item in interviews:
                interview = Interview.objects.create(
                    trainee=trainee, company_name=item['company_name'], interview_date=item['interview_date'], status=item['status'],
                    designation_offered=item.get('designation_offered'), salary_ctc=item.get('salary_ctc'), 
                    current_household_income=item.get('current_household_income')
                )

                created.append(InterviewSerializer(interview).data)

        return Response(created)


class RetentionViewSet(viewsets.ModelViewSet):

    queryset = Retention.objects.all()
    serializer_class = RetentionSerializer
    permission_classes = [IsAdminPlacement]

    @action(detail=False, methods=['post'], url_path='bulk-update')
    def bulk_update(self, request):
        # POST /api/placement/retention/bulk-update/
        trainee_id = request.data.get('trainee')
        months = request.data.get('months', [])

        try:
            trainee = Trainee.objects.get(id=trainee_id)

        except Trainee.DoesNotExist:
            return Response(
                {
                    "error":
                    "Invalid trainee."
                },
                status=404
            )

        selected = Interview.objects.filter(trainee=trainee, status='Selected').exists()

        if not selected:
            return Response(
                {
                    "error":
                    "Student not selected in Interview."
                },
                status=400
            )

        records = []

        with transaction.atomic():
            for item in months:
                retention, _ = (Retention.objects.update_or_create(
                    trainee=trainee, month_number=item['month_number'],
                    defaults={
                            'retention_status':item['retention_status'],
                            'remarks':item.get('remarks', '')
                             }
                    )
                )

                records.append(RetentionSerializer(retention).data)

        return Response(records)

class RetentionRecordListView(ListAPIView):
    # GET /api/placement/retention-records/
    serializer_class = RetentionRecordSerializer
    permission_classes = [IsAdminPlacement]

    def get_queryset(self):
        return Trainee.objects.filter(interviews__status='Selected').distinct()