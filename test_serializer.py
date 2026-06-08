import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from placement.serializers import PlacementCandidateSerializer
from onboarding.models import Trainee

try:
    trainees = Trainee.objects.all()
    serializer = PlacementCandidateSerializer(trainees, many=True)
    data = serializer.data
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
