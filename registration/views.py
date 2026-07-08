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
        if self.action == 'destroy':
            return [IsAdminOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        '''
        Filtering by:domain,counsellor,ward,slot,center
        '''
        queryset = Registration.objects.all()
        
        if self.request.user.role == 'counsellor':
            queryset = queryset.filter(registered_by=self.request.user)

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
        from rest_framework import serializers as drf_serializers
        counselling_log = serializer.validated_data['counselling_log']

        if counselling_log.status != 'Interested':
            raise drf_serializers.ValidationError(
                {'error': 'Only Interested students can register.'}
            )

        if Registration.objects.filter(counselling_log=counselling_log).exists():
            raise drf_serializers.ValidationError(
                {'error': 'This student is already registered.'}
            )

        mobilization = getattr(counselling_log, 'mobilization_record', None)
        qualifications = mobilization.qualifications.all() if mobilization and hasattr(mobilization, 'qualifications') else []

        highest_qualification = None

        if qualifications and qualifications.exists():
            highest_qualification = qualifications.order_by('-sl_no').first().exam_name

        center = serializer.validated_data.get('center') or self.request.data.get('center') or 'Faridabad'
        center_code = str(center)[:3].upper()

        serial = Registration.objects.count() + 1

        registration_id = (f"HSU/{center_code}/{serial:03d}")

        req_data = self.request.data
        name = (mobilization.name if mobilization else None) or req_data.get('name') or 'Unknown'
        mobile = (mobilization.mobile if mobilization else None) or req_data.get('mobile') or ''
        gender = (mobilization.gender if mobilization else None) or req_data.get('gender') or ''
        father_name = (mobilization.father_name if mobilization else None) or req_data.get('father_name') or ''
        dob = (mobilization.dob if mobilization else None) or req_data.get('dob') or None
        if dob == '':
            dob = None
        ward_no = (mobilization.ward_no if mobilization else None) or req_data.get('ward_no') or ''
        pin = (mobilization.pin if mobilization else None) or req_data.get('pin') or ''
        slot = counselling_log.slot or req_data.get('slot') or ''
        domain = counselling_log.domain or req_data.get('domain') or ''
        counselled_by_name = counselling_log.counselled_by_name or req_data.get('counselled_by_name') or ''
        counselling_date = counselling_log.date or req_data.get('counselling_date') or None
        if counselling_date == '':
            counselling_date = None

        serializer.save(
            registration_id = registration_id,
            registered_by = self.request.user,
            name = name,
            mobile = mobile,
            gender = gender,
            father_name = father_name,
            dob = dob,
            ward_no = ward_no,
            pin = pin,
            slot = slot,
            domain = domain,
            counselled_by_name = counselled_by_name,
            counselling_date = counselling_date,
            education = highest_qualification or req_data.get('education') or ''
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
        base_queryset = Registration.objects.all()
        queryset = base_queryset

        if request.user.role == 'counsellor':
            queryset = queryset.filter(registered_by=request.user)

        total_registered = queryset.count()
        female_enrolled = queryset.filter(gender='Female').count()
        morning_slot = queryset.filter(slot='Morning').count()
        evening_slot = queryset.filter(slot='Evening').count()

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
            for item in (base_queryset.values("counselled_by_name").annotate(count=Count("id")).order_by("-count"))
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
            "kpis": {
                "total_registered": total_registered,
                "female_enrolled": female_enrolled,
                "morning_slot": morning_slot,
                "evening_slot": evening_slot,
            },
            "charts": {
                "domain_registration":domain_registration,
                "counsellor_registration":counsellor_registration,
                "ward_registration":ward_registration,
                "gender_enrolment":gender_enrolment
            }
        })