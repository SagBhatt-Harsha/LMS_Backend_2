from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Registration
from .serializers import (RegistrationSerializer, RegistrationSearchSerializer)

from .permissions import (IsAdminCounsellorTeacher, IsAdminCounsellor, IsAdminOnly)

# Create your views here.

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()

    def get_serializer_class(self):
        if self.action == 'search':
            return RegistrationSearchSerializer

        return RegistrationSerializer


    def get_permissions(self):
        if self.action == 'update':
            return [IsAdminCounsellor()]

        elif self.action == 'destroy':
            return [IsAdminOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        # Filtering by domain,slot and center.
        queryset = Registration.objects.all()

        domain = self.request.query_params.get('domain')
        slot = self.request.query_params.get('slot')
        center = self.request.query_params.get('center')

        if domain:
            queryset = queryset.filter(domain=domain)

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