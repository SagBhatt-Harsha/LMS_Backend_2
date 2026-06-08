import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from placement.views import PlacementCandidateListView
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
request = factory.get('/api/placement/candidates/')
view = PlacementCandidateListView.as_view()

try:
    response = view(request)
    print("STATUS:", response.status_code)
    print("DATA:", response.data)
except Exception as e:
    import traceback
    traceback.print_exc()
