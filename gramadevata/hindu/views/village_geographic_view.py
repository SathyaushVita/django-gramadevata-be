from rest_framework import viewsets, permissions
from ..models import Geographic
from ..serializers import VillageGeographicSerializer,InactiveVillageGeographicSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class VillageGeographicViewSet(viewsets.ModelViewSet):
    queryset = Geographic.objects.all()
    serializer_class = VillageGeographicSerializer









class InactiveGeographicAPIView(APIView):
    """
    API to get only INACTIVE Geographic entries
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE geographic entries
        queryset = Geographic.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by village name, ancient_name, or under_panchayat
        if search_query:
            queryset = queryset.filter(
                Q(ancient_name__icontains=search_query) |
                Q(village_id__name__icontains=search_query) |
                Q(under_panchayat__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveVillageGeographicSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_geographic": serializer.data
        }, status=status.HTTP_200_OK)