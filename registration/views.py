from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

from .models import Registration
from .serializers import (RegistrationSerializer, RegistrationSearchSerializer)

from .permissions import (IsAdminCounsellorTeacher, IsAdminOnly)

# Create your views here.

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()

    def get_serializer_class(self):
        if self.action == 'search':
            return RegistrationSearchSerializer

        return RegistrationSerializer


    def get_permissions(self):
        if self.action in ['destroy', 'analytics']:
            return [IsAdminOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        '''
        Filtering by:domain,counsellor,ward,slot,center
        '''
        queryset = Registration.objects.all()

        domain = self.request.query_params.get('domain')
        counsellor = self.request.query_params.get('counsellor')

        ward = self.request.query_params.get('ward')
        slot = self.request.query_params.get('slot')
        center = self.request.query_params.get('center')

        if domain:
            queryset = queryset.filter(domain=domain)

        if counsellor:
            queryset = queryset.filter(counselled_by_name=counsellor)

        if ward:
            queryset = queryset.filter(ward_no=ward)

        if slot:
            queryset = queryset.filter(slot=slot)

        if center:
            queryset = queryset.filter(center=center)

        return queryset

    def perform_create(self, serializer):
        counselling_log = serializer.validated_data['counselling_log']

        if counselling_log.status != 'Interested':
            raise ValueError(
                'Only Interested students can register.'
            )

        mobilization = counselling_log.mobilization_record
        qualifications = mobilization.qualifications.all()

        highest_qualification = None

        if qualifications.exists():
            highest_qualification = qualifications.order_by('-sl_no').first().exam_name
            # Highest sl_no's exam_name will be assigned to highest_qualification.

        center = serializer.validated_data['center']
        center_code = center[:3].upper()

        serial = Registration.objects.count() + 1

        registration_id = (f"HSU/{center_code}/{serial:03d}")

        serializer.save(
            registration_id = registration_id,
            registered_by = self.request.user,
            name = mobilization.name,
            mobile = mobilization.mobile,
            gender = mobilization.gender,
            father_name = mobilization.father_name,
            dob = mobilization.dob,
            ward_no = mobilization.ward_no,
            pin = mobilization.pin,
            slot = counselling_log.slot,
            domain = counselling_log.domain,
            counselled_by_name = counselling_log.counselled_by_name,
            counselling_date = counselling_log.date,
            education = highest_qualification
        )

        # Setting the enrolled_flag true for Counselled Students who have been registered. 
        counselling_log.enrolled_flag = True
        counselling_log.save(update_fields=['enrolled_flag'])


    @action(detail=False, methods=['get'])
    def search(self, request):
        # Custom Search API: GET /api/registration/search/?mobile=
        mobile = request.query_params.get('mobile')

        try:
            registration = Registration.objects.get(mobile=mobile)
            serializer = self.get_serializer(registration)
            return Response(serializer.data)

        except Registration.DoesNotExist:
            return Response(
                {
                    "error":
                    "No registration found for this mobile number"
                },
                status=404
            )

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        # Analytics API: GET /api/registration/analytics
        queryset = Registration.objects.all()

        domain_registration = [
            {
                "domain": item["domain"],
                "count": item["count"]
            }
            for item in (queryset.exclude(domain__isnull=True).values("domain").annotate(count=Count("id")).order_by("-count"))
        ]

        counsellor_registration = [
            {
                "counsellor_name": item["counselled_by_name"],
                "count": item["count"]
            }
            for item in (queryset.values("counselled_by_name").annotate(count=Count("id")).order_by("-count"))
        ]

        ward_registration = [
            {
                "ward": item["ward_no"],
                "count": item["count"]
            }
            for item in (queryset.values("ward_no").annotate(count=Count("id")).order_by("-count"))
        ]

        gender_enrolment = [
            {
                "gender": item["gender"],
                "count": item["count"]
            }
            for item in (queryset.values("gender").annotate(count=Count("id")).order_by("-count"))
        ]

        return Response({

            "charts": {
                "domain_registration":domain_registration,
                "counsellor_registration":counsellor_registration,
                "ward_registration":ward_registration,
                "gender_enrolment":gender_enrolment
            }
        })