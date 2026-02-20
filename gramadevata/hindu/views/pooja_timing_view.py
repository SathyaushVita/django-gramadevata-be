from rest_framework import viewsets
from rest_framework.response import Response
from ..models import TemplePoojaTiming
from ..serializers import TemplePoojaTimingSerializer

class TemplePoojaTimingViewSet(viewsets.ModelViewSet):
    queryset = TemplePoojaTiming.objects.all()
    serializer_class = TemplePoojaTimingSerializer

    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always filter ACTIVE status
        filter_kwargs['status'] = 'ACTIVE'

        queryset = TemplePoojaTiming.objects.filter(**filter_kwargs)

        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            })

        serialized_data = TemplePoojaTimingSerializer(queryset, many=True)
        return Response(serialized_data.data)

    def retrieve(self, request, pk=None):
        try:
            instance = TemplePoojaTiming.objects.get(_id=pk, status='ACTIVE')
            serializer = TemplePoojaTimingSerializer(instance)
            return Response(serializer.data, status=200)
        except TemplePoojaTiming.DoesNotExist:
            return Response({
                'message': 'Pooja timing record not found',
                'status': 404
            }, status=404)
