from rest_framework import viewsets
from .models import Teacher
from .serializers import TeacherSerializer
from .permissions import IsAdminCounsellorTeacher

# Create your views here.

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_permissions(self):
        return [IsAdminCounsellorTeacher()]

    def get_queryset(self):
        # Filtering by domain
        queryset = Teacher.objects.all()
        domain = self.request.query_params.get('domain')

        if domain:
            queryset = queryset.filter(domain=domain)

        return queryset