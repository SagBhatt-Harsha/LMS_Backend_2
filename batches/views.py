from django.utils.timezone import now
from rest_framework import viewsets
from .models import Batch
from .serializers import BatchSerializer
from .permissions import IsAdminCounsellorTeacher, IsAdminOnly

# Create your views here.
class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminOnly()]

        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        queryset = Batch.objects.all()

        domain = self.request.query_params.get('domain')
        slot = self.request.query_params.get('slot')

        active = self.request.query_params.get('active')

        if domain:
            queryset = queryset.filter(domain=domain)

        if slot:
            queryset = queryset.filter(slot=slot)

        if active == 'true':
            queryset = queryset.filter(end_date__gte=now().date())

        if active == 'false':
            queryset = queryset.filter(end_date__lt=now().date())

        return queryset


    def perform_create(self, serializer):
        # Batch Name Auto Generation for POST
        domain = serializer.validated_data['domain']
        slot = serializer.validated_data['slot']

        count = Batch.objects.filter(domain=domain, slot=slot).count() + 1

        batch_name = f"{domain} {slot} Batch {count}"
        serializer.save(name=batch_name)


    def perform_update(self, serializer):
        # Batch Name Auto Generation for PUT
        domain = serializer.validated_data.get('domain', serializer.instance.domain)
        slot = serializer.validated_data.get('slot', serializer.instance.slot)

        count = Batch.objects.filter(domain=domain, slot=slot).exclude(id=serializer.instance.id).count() + 1

        batch_name = f"{domain} {slot} Batch {count}"
        serializer.save(name=batch_name)