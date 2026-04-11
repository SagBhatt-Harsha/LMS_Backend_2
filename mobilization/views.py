from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MobilizationRecord
from .serializers import MobilizationSerializer
from .permissions import (IsNotTrainee, IsAdminOrMobilizer, IsAdminOrOwnerMobilizer)


class MobilizationViewSet(viewsets.ModelViewSet):

    queryset = MobilizationRecord.objects.all()

    serializer_class = MobilizationSerializer


    def get_permissions(self):
        # Dynamic permission by Kind of Authenticated User.
        if self.action == 'create': 
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
        # For Filtering by state & created_by.
        # GET /api/mobilization/?state=
        # GET /api/mobilization/?created_by=
        queryset = MobilizationRecord.objects.all()

        state = self.request.query_params.get('state')

        created_by = self.request.query_params.get('created_by')

        if state:
            queryset = queryset.filter(state=state)

        if created_by:
            queryset = queryset.filter(created_by=created_by)

        return queryset


    def perform_create(self, serializer):
        # perform_create() method deals with Current Authenticated User data.
        # Defines What will be stored in added_by_name and created_by variables.
        # created_by stores Current Authenticated User id.
        # added_by_name stores Current Authenticated User's name.
        serializer.save(
            created_by=self.request.user,
            added_by_name=self.request.user.name
        )


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