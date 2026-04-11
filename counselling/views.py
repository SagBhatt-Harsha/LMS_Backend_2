from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CounsellingLog

from .serializers import (CounsellingSerializer, CounsellingStatusUpdateSerializer)

from .permissions import (IsAdminCounsellorTeacher, IsAdminOnly)


# Create your views here.


class CounsellingViewSet(viewsets.ModelViewSet):

    queryset = CounsellingLog.objects.all()

    def get_serializer_class(self):
        # For GET, PUT, POST, PATCH, DELETE, CounsellingSerializer will be used through serializer_class. For the custom PATCH API endpoint, CounsellingStatusUpdateSerializer will be used.
        if self.action == 'status':
            return CounsellingStatusUpdateSerializer

        return CounsellingSerializer


    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminCounsellorTeacher()]

        elif self.action == 'destroy':
            return [IsAdminOnly()]

        elif self.action == 'status':
            return [IsAdminCounsellorTeacher()]

        return [IsAdminCounsellorTeacher()] 


    def get_queryset(self):
        # For Filtering by status or counselled_by
        queryset = CounsellingLog.objects.all()

        status = self.request.query_params.get('status')

        counselled_by = self.request.query_params.get('counselled_by')

        if status:
            queryset = queryset.filter(status=status)

        if counselled_by:
            queryset = queryset.filter(counselled_by=counselled_by)

        return queryset


    def perform_create(self, serializer):
        serializer.save(
            counselled_by=self.request.user,
            counselled_by_name=self.request.user.name
        )


    @action(detail=True, methods=['patch'], url_path='status')
    def status(self, request, pk=None):
        # Custom PATCH API: PATCH /api/counselling/{id}/status/
        counselling = self.get_object()

        serializer = self.get_serializer(counselling, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)