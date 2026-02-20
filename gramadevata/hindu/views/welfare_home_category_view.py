from rest_framework import viewsets
from rest_framework.response import Response
from ..models import WelfareHomesCategory
from ..serializers import WelfareHomesCategorySerializer



class WelfareHomesCategoryViewSet(viewsets.ModelViewSet):
    queryset = WelfareHomesCategory.objects.all()
    serializer_class = WelfareHomesCategorySerializer


    
    def get_queryset(self):
        # Order by priority first, then created_at for consistent ordering
        return WelfareHomesCategory.objects.all().order_by('priority', '-created_at')