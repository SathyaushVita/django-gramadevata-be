from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import TempleTransport
from ..serializers import TempleTransportSerializer,InactiveTransportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


class TempleTransportViewSet(viewsets.ModelViewSet):
    queryset = TempleTransport.objects.all()
    serializer_class = TempleTransportSerializer
    # permission_classes = []

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def list(self, request):
        filter_kwargs = {}

        # Apply query parameter filters
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always ensure status is ACTIVE for listing
        filter_kwargs['status'] = 'ACTIVE'

        queryset = TempleTransport.objects.filter(**filter_kwargs)

        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            })

        serialized_data = TempleTransportSerializer(queryset, many=True)
        return Response(serialized_data.data)




    def retrieve(self, request, pk=None):
        try:
            instance = TempleTransport.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=200)
        except TempleTransport.DoesNotExist:
            return Response({
                'message': 'Transport record not found',
                'status': 404
            }, status=404)







class InactiveTransportAPIView(APIView):


    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        queryset = TempleTransport.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        if search_query:
            queryset = queryset.filter(
                Q(temple_id__name__icontains=search_query) |
                Q(village_id__name__icontains=search_query) |
                Q(transport_type__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveTransportSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_temple_transport": serializer.data
        }, status=status.HTTP_200_OK)