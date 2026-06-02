from django.utils.timezone import now
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from mobilization.models import MobilizationRecord
from counselling.models import CounsellingLog
from registration.models import Registration
from onboarding.models import Trainee
from batches.models import Batch

# Create your views here.
class DashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'admin':
            return Response(self.get_admin_metrics())

        elif user.role == 'mobilizer':
            return Response(self.get_mobilizer_metrics(user))

        elif user.role == 'counsellor':
            return Response(self.get_counsellor_metrics(user))

        return Response({})

    def get_admin_metrics(self):
        total_mobilized = MobilizationRecord.objects.count()
        total_counselled = CounsellingLog.objects.count()
        total_interested = CounsellingLog.objects.filter(status='Interested').count()
        total_registered = Registration.objects.count()
        total_onboarded = Trainee.objects.count()

        gender_distribution = dict(MobilizationRecord.objects.values_list('gender').annotate(count=Count('id')))

        caste_distribution = dict(MobilizationRecord.objects.values_list('caste').annotate(count=Count('id')))

        counselling_status_breakdown = dict(CounsellingLog.objects.values_list('status').annotate(count=Count('id')))

        domain_distribution = dict(CounsellingLog.objects.filter(status='Interested').values_list('domain').annotate(count=Count('id')))

        top_states = list(MobilizationRecord.objects.values('state').annotate(count=Count('id')).order_by('-count')[:5])

        pipeline_funnel = {
            "mobilized": total_mobilized,
            "counselled": total_counselled,
            "interested": total_interested,
            "registered": total_registered,
            "onboarded": total_onboarded
        }

        active_batches = Batch.objects.filter(end_date__gte=now().date()).count()
        closed_batches = Batch.objects.filter(end_date__lt=now().date()).count()

        batch_utilization = []
        for batch in Batch.objects.filter(end_date__gte=now().date()):
            batch_utilization.append({
                "id": batch.id,
                "name": batch.name,
                "domain": batch.domain,
                "slot": batch.slot,
                "capacity": batch.capacity,
                "enrolled": batch.trainees.count()
            })

        recent_mobilizations = list(MobilizationRecord.objects.values('id', 'name', 'mobile', 'state', 'date').order_by('-date')[:5])


        return {
            "total_mobilized": total_mobilized,
            "total_counselled": total_counselled,
            "total_interested": total_interested,
            "total_registered": total_registered,
            "total_onboarded": total_onboarded,
            "gender_distribution": gender_distribution,
            "caste_distribution": caste_distribution,
            "counselling_status_breakdown": counselling_status_breakdown,
            "domain_distribution": domain_distribution,
            "top_states": top_states,
            "pipeline_funnel": pipeline_funnel,
            "active_batches": active_batches,
            "closed_batches": closed_batches,
            "batch_utilization": batch_utilization,
            "recent_mobilizations": recent_mobilizations
        }


    def get_mobilizer_metrics(self, user):
        mobilizations = MobilizationRecord.objects.filter(created_by=user)
        total_mobilized = mobilizations.count()
        
        female_students = mobilizations.filter(gender='Female').count()
        sc_st_students = mobilizations.filter(caste__in=['SC', 'ST']).count()
        wards_covered = mobilizations.values('ward_no').distinct().count()
        
        counselled_count = mobilizations.filter(counselling_converted=True).count()
        conversion_rate = round((counselled_count / total_mobilized * 100), 2) if total_mobilized > 0 else 0

        recent_records = mobilizations.order_by('-date', '-id')[:6]
        recent_list = []
        for r in recent_records:
            c_log = CounsellingLog.objects.filter(mobilization_record=r).first()
            recent_list.append({
                "id": r.id,
                "name": r.name,
                "mobile": r.mobile,
                "gender": r.gender,
                "caste": r.caste,
                "ward_no": r.ward_no,
                "date": r.date,
                "state": r.state,
                "counselling_status": c_log.status if c_log else "Pending Counselling",
                "domain_preference": c_log.domain if c_log and c_log.domain else "—"
            })

        return {
            "total_mobilized": total_mobilized,
            "female_students": female_students,
            "sc_st_students": sc_st_students,
            "wards_covered": wards_covered,
            "counselled_count": counselled_count,
            "conversion_rate": conversion_rate,
            "gender_distribution": dict(mobilizations.values_list('gender').annotate(count=Count('id'))),
            "caste_distribution": dict(mobilizations.values_list('caste').annotate(count=Count('id'))),
            "top_states": list(mobilizations.values('state').annotate(count=Count('id')).order_by('-count')[:5]),
            "recent_mobilizations": recent_list
        }


    def get_counsellor_metrics(self, user):
        counselling = CounsellingLog.objects.filter(counselled_by=user)
        total_counselled = counselling.count()

        female_students = counselling.filter(mobilization_record__gender='Female').count()
        sc_st_students = counselling.filter(mobilization_record__caste__in=['SC', 'ST']).count()
        wards_covered = counselling.values('mobilization_record__ward_no').distinct().count()

        enrolled_count = counselling.filter(enrolled_flag=True).count()
        conversion_rate = round((enrolled_count / total_counselled * 100), 1) if total_counselled > 0 else 0

        domain_distribution = dict(counselling.filter(status='Interested').values_list('domain').annotate(count=Count('id')))
        slot_distribution = dict(counselling.filter(status='Interested').values_list('slot').annotate(count=Count('id')))

        recent_records = counselling.order_by('-date', '-id')[:6]
        recent_list = []
        for r in recent_records:
            recent_list.append({
                "id": r.id,
                "name": r.name,
                "mobile": r.mobile,
                "gender": r.mobilization_record.gender if r.mobilization_record else "—",
                "date": r.date,
                "slot": r.slot,
                "domain_preference": r.domain,
                "status": r.status,
                "enrolled_flag": r.enrolled_flag
            })

        return {
            "total_counselled": total_counselled,
            "female_students": female_students,
            "sc_st_students": sc_st_students,
            "wards_covered": wards_covered,
            "enrolled_count": enrolled_count,
            "conversion_rate": conversion_rate,
            "counselling_status_breakdown": dict(counselling.values_list('status').annotate(count=Count('id'))),
            "domain_distribution": domain_distribution,
            "slot_distribution": slot_distribution,
            "recent_counselling": recent_list
        }