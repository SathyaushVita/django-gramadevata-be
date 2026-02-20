from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import TempleTransport
from ..serializers import TempleTransportSerializer

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
