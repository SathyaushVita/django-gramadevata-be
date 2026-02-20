from rest_framework import viewsets, permissions
from ..models import Geographic
from ..serializers import VillageGeographicSerializer

class VillageGeographicViewSet(viewsets.ModelViewSet):
    queryset = Geographic.objects.all()
    serializer_class = VillageGeographicSerializer