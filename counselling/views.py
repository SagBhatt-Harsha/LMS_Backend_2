from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CounsellingLog

from .serializers import (CounsellingSerializer, CounsellingStatusUpdateSerializer)

from .permissions import (IsAdminCounsellorTeacher, IsAdminOnly, IsAdminCounsellor)

from registration.models import Registration

# Create your views here.


class CounsellingViewSet(viewsets.ModelViewSet):

    queryset = CounsellingLog.objects.all()

    def get_serializer_class(self):
        # For GET, PUT, POST, PATCH, DELETE, CounsellingSerializer will be used through serializer_class. For the custom PATCH API endpoint, CounsellingStatusUpdateSerializer will be used.
        if self.action == 'status':
            return CounsellingStatusUpdateSerializer

        return CounsellingSerializer


    def get_permissions(self):
        if self.action == 'analytics':
            return [IsAdminCounsellorTeacher()]
        
        if self.action == 'create':
            return [IsAdminCounsellorTeacher()]

        elif self.action == 'destroy':
            return [IsAdminCounsellor()]

        elif self.action == 'status':
            return [IsAdminCounsellorTeacher()]

        return [IsAdminCounsellorTeacher()]


    def get_queryset(self):
        # ModelViewSet automatically calls this method whenever a GET request is made.
        '''For Filtering(by status or counselled_by_name or slot or domain or gender or status)'''

        # Sync old records that already have Registration entries
        registration_ids = Registration.objects.values_list('counselling_log_id', flat=True)
        CounsellingLog.objects.filter(id__in=registration_ids,enrolled_flag=False).update(enrolled_flag=True)
        
        queryset = CounsellingLog.objects.all()

        counsellor = self.request.query_params.get('counsellor')

        domain = self.request.query_params.get('domain')
        slot = self.request.query_params.get('slot')
        status = self.request.query_params.get('status')

        gender = self.request.query_params.get('gender')

        if counsellor:
            queryset = queryset.filter(counselled_by_name=counsellor)

        if domain:
            queryset = queryset.filter(domain=domain)

        if slot:
            queryset = queryset.filter(slot=slot)

        if gender:
            queryset = queryset.filter(mobilization_record__gender=gender)

        if status:
            queryset = queryset.filter(status=status)

        return queryset


    def perform_create(self, serializer):
        '''Saves the id and name of Current Logged in User who is Creating the Counselling Log(Counsellor Permission).
           Also Auto-updates the counselling_converted flag to True when a mobilised student is counselled(put into CounsellingLog)'''
        mobilization_record = serializer.validated_data['mobilization_record']
        # Above line is to change the counselling_converted Flag to True for the mobilized Student who has gone through Counselling.
        
        serializer.save(counselled_by=self.request.user, counselled_by_name=self.request.user.name)

        mobilization_record.counselling_converted = True
        mobilization_record.save()

    
    @action(detail=True, methods=['patch'], url_path='status')
    def status(self, request, pk=None):
        # Custom PATCH API: PATCH /api/counselling/{id}/status/
        counselling = self.get_object()

        serializer = self.get_serializer(counselling, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        # GET /api/counselling/analytics
        base_queryset = CounsellingLog.objects.all()
        queryset = base_queryset
        if request.user.role == 'counsellor':
            queryset = queryset.filter(counselled_by=request.user)

        total_counselled = queryset.count()

        female_students = queryset.filter(mobilization_record__gender='Female').count()

        sc_st_students = queryset.filter(mobilization_record__caste__in=['SC', 'ST']).count()

        wards_covered = queryset.values('mobilization_record__ward_no').distinct().count()

        enrolled_count = queryset.filter(enrolled_flag=True).count()

        if total_counselled > 0:
            conversion_to_enrolment = (round(enrolled_count * 100 / total_counselled, 2))
        
        else:
            conversion_to_enrolment = 0

        ward_breakdown = [
            {
                "ward":item["mobilization_record__ward_no"],
                "count":item["count"],
                "enrolled":item["enrolled"]
            }
            for item in (queryset.values("mobilization_record__ward_no").annotate(count=Count("id"), enrolled=Count("id", filter=Q(enrolled_flag=True))).order_by("-count"))
        ]

        domain_preference = [
            {
                "domain":item["domain"],
                "count":item["count"],
                "enrolled":item["enrolled"]
            }
            for item in (queryset.exclude(domain__isnull=True).values("domain").annotate(count=Count("id"), enrolled=Count("id", filter=Q(enrolled_flag=True))).order_by("-count"))
        ]

        counsellor_sessions = [
            {
                "counsellor_name":item["counselled_by_name"],
                "count":item["count"],
                "enrolled":item["enrolled"],
                "female":item["female"],
                "sc_st":item["sc_st"],
                "wards_covered":item["wards_covered"],
                "interested":item["interested"],
                "not_interested":item["not_interested"],
                "decision_pending":item["decision_pending"],
            }
            for item in (base_queryset.values("counselled_by_name").annotate(
                count=Count("id"),
                enrolled=Count("id", filter=Q(enrolled_flag=True)),
                female=Count("id", filter=Q(mobilization_record__gender='Female')),
                sc_st=Count("id", filter=Q(mobilization_record__caste__in=['SC', 'ST'])),
                wards_covered=Count("mobilization_record__ward_no", distinct=True),
                interested=Count("id", filter=Q(status='Interested')),
                not_interested=Count("id", filter=Q(status='Not Interested')),
                decision_pending=Count("id", filter=Q(status='Decision Pending')),
            ).order_by("-count"))
        ]

        slot_distribution = [
            {
                "slot":item["slot"],
                "count":item["count"]
            }
            for item in (queryset.exclude(domain__isnull=True).values("slot").annotate(count=Count("id")))
        ]

        return Response({

            "kpis": {
                "total_counselled": total_counselled,
                "female_students": female_students,
                "sc_st_students": sc_st_students,
                "wards_covered": wards_covered,
                "conversion_to_enrolment":conversion_to_enrolment
            },

            "charts": {
                "ward_breakdown":ward_breakdown,
                "domain_preference":domain_preference,
                "counsellor_sessions":counsellor_sessions,
                "slot_distribution":slot_distribution
            }
        })