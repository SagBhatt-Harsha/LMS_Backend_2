from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MobilizationRecord
from .serializers import MobilizationSerializer
from .permissions import (IsNotTrainee, IsAdminOrMobilizer, IsAdminOrOwnerMobilizer, IsAdminOnly)

from counselling.models import CounsellingLog

# Create your views here.
class MobilizationViewSet(viewsets.ModelViewSet):

    queryset = MobilizationRecord.objects.all()
    serializer_class = MobilizationSerializer

    def get_permissions(self):
        # Dynamic permission by Kind of Authenticated User.
        if self.action == 'analytics':
            return [IsAdminOrMobilizer()]

        elif self.action == 'create': 
            # POST
            return [IsAdminOrMobilizer()]

        elif self.action == 'update':
            # PUT
            return [IsAdminOrMobilizer(), IsAdminOrOwnerMobilizer()]

        elif self.action == 'partial_update':
            # PATCH
            return [IsAdminOrMobilizer(), IsAdminOrOwnerMobilizer()]

        elif self.action == 'destroy':
            # DELETE
            return [IsAdminOrMobilizer(), IsAdminOrOwnerMobilizer()]

        return [IsNotTrainee()]


    def get_queryset(self):
        '''ModelViewSet automatically calls this method whenever a GET request is made.'''
        # For Filtering by state,ward,gender,mobilizer_name
        # GET /api/mobilization/?state=
        # GET /api/mobilization/?mobilizer=
        # GET /api/mobilization/?ward=
        # GET /api/mobilization/?gender=

        # One-time sync of old records
        counselling_ids = CounsellingLog.objects.values_list('mobilization_record_id', flat=True)
        # We are giving mobilization_record_id even though FK name in counselling table/model is mobilization_record. This is becz Django auto-adds the _id part(bts) with any FK name specefied.

        MobilizationRecord.objects.filter(id__in=counselling_ids, counselling_converted=False).update(counselling_converted=True)
        '''Above two lines of code are used to set the counselling_converted flag of existing Mob.Students to True if false for any of them.'''

        queryset = MobilizationRecord.objects.all()
        if hasattr(self.request.user, 'role') and self.request.user.role == 'mobilizer':
            queryset = queryset.filter(created_by=self.request.user)
            
        state = self.request.query_params.get('state')
        # self.request.query_params.get('state') Extracts the state(?state=) from GET Request.

        mobiliser = self.request.query_params.get('mobiliser')
        ward = self.request.query_params.get('ward')
        gender = self.request.query_params.get('gender')

        if mobiliser:
            queryset = queryset.filter(added_by_name=mobiliser)

        if ward:
            queryset = queryset.filter(ward_no=ward)

        if gender:
            queryset = queryset.filter(gender__iexact=gender) # Lower-case Comparison(by using iexact Field Lookup)

        if state:
            queryset = queryset.filter(state=state)

        return queryset


    def perform_create(self, serializer):
        # POST Request(Auto-called by DRF after POST Request)
        # perform_create() method deals with Current Authenticated User data.
        # Defines What will be stored in added_by_name and created_by variables.
        # created_by stores Current Authenticated User id.
        # added_by_name stores Current Authenticated User's name.

        serializer.save(created_by=self.request.user, added_by_name=self.request.user.name)


    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        # Custom Search API Endpoint: GET /api/mobilization/search/?mobile=
        mobile = request.query_params.get('mobile')

        try:
            record = MobilizationRecord.objects.get(mobile=mobile)
            serializer = self.get_serializer(record)
            return Response(serializer.data)

        except MobilizationRecord.DoesNotExist:
            return Response(
                {
                    "error":
                    "No record found for this mobile number"
                },
                status=404
            )

    # Analytics API Endpoint: GET /mobilization/analytics/
    @action(detail=False, methods=['get'])
    def analytics(self, request):

        queryset = self.get_queryset()

        total_mobilised = queryset.count()
        female_students = queryset.filter(gender='Female').count()
        sc_st_students = queryset.filter(caste__in=['SC', 'ST']).count()
        wards_covered = queryset.values('ward_no').distinct().count()

        converted_count = queryset.filter(counselling_converted=True).count()

        if total_mobilised > 0:
            conversion_rate = (round(converted_count * 100 / total_mobilised, 2))
        else:
            conversion_rate = 0
        
        # List Comprehension with Django ORM used below.
        '''
        queryset.values("ward_no").annotate(count=Count("id")).order_by("-count"): queryset refers to all Records/tuples in table. 
        values("ward_no") Keeps only the ward_no Column.
        annotate(count=Count("id") counts how many records exist and stores it in count Column when Django groups the records by the field used in values() Function.
        order_by("-count") simply orders the dics in desc. order of count
        The Entire Expression returns a Queryset of Dictionaries where item points to each dictionary.
        '''

        from django.db.models import Count, Q, FloatField
        from django.db.models.functions import Cast
        
        ward_data = queryset.values('ward_no').annotate(
            total=Count('id'),
            female=Count('id', filter=Q(gender='Female')),
            male=Count('id', filter=Q(gender='Male')),
            sc_st=Count('id', filter=Q(caste__in=['SC', 'ST'])),
            counselled=Count('id', filter=Q(counselling_converted=True))
        ).order_by('-total')

        ward_breakdown = []
        for item in ward_data:
            conv_pct = round((item['counselled'] * 100.0) / item['total']) if item['total'] > 0 else 0
            ward_breakdown.append({
                "ward": item["ward_no"],
                "count": item["total"],
                "female": item["female"],
                "male": item["male"],
                "sc_st": item["sc_st"],
                "counselled": item["counselled"],
                "conversion": conv_pct
            })

        mobiliser_breakdown = [
            {
                "mobiliser_name":item["added_by_name"],
                "count":item["count"]
            }
            for item in (queryset.values("added_by_name").annotate(count=Count("id")).order_by("-count"))
        ]

        gender_breakdown = list(queryset.values("gender").annotate(count=Count("id")))
        caste_breakdown = list(queryset.values("caste").annotate(count=Count("id")))

        return Response({
            "kpis": {
                "total_mobilised": total_mobilised,
                "female_students": female_students,
                "sc_st_students": sc_st_students,
                "wards_covered": wards_covered,
                "conversion_rate": conversion_rate
            },
            "charts": {
                "ward_breakdown": ward_breakdown,
                "mobiliser_breakdown": mobiliser_breakdown,
                "gender_breakdown": gender_breakdown,
                "caste_breakdown": caste_breakdown
            }
        })