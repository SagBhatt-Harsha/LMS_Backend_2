from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Trainee
from .serializers import TraineeSerializer, BatchAssignSerializer, BatchAssignResponseSerializer
from .permissions import IsAdminCounsellorTeacher, IsAdminOnly

# Create your views here.
class TraineeViewSet(viewsets.ModelViewSet):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer

    def get_serializer_class(self):
        if self.action == 'batch':
            return BatchAssignSerializer

        return TraineeSerializer


    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        # Filtering by batch,domain,slot.
        queryset = Trainee.objects.all()

        batch = self.request.query_params.get('batch')

        domain = self.request.query_params.get('domain')

        slot = self.request.query_params.get('slot')

        if batch:
            queryset = queryset.filter(batch=batch)

        if domain:
            queryset = queryset.filter(domain=domain)

        if slot:
            queryset = queryset.filter(slot=slot)

        return queryset


    def perform_create(self, serializer):
        registration = serializer.validated_data['registration']

        if hasattr(registration, 'trainee'):
            raise ValidationError("This registration is already onboarded.")

        serializer.save(
            registration_code = registration.registration_id,
            name = registration.name,
            gender = registration.gender,
            contact = registration.mobile,
            slot = registration.slot,
            domain = registration.domain,
            education = registration.education,
            address = registration.address,
            registered_by = self.request.user
        )


    @action(detail=True, methods=['patch'], url_path='batch')
    def batch(self, request, pk=None):
        # Custom PATCH API endpoint.
        trainee = self.get_object()
        serializer = BatchAssignSerializer(trainee, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_serializer = BatchAssignResponseSerializer(trainee)
        return Response(response_serializer.data)