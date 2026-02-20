from ..serializers import PujariCategeorySerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import PujariCategory


class PujariCategeoryview(viewsets.ModelViewSet):
    queryset = PujariCategory.objects.all()
    serializer_class = PujariCategeorySerializer

    def list(self, request):
        try:
            queryset = self.queryset

            # Handle multiple filter conditions (e.g., ?_id=1,2,3 or ?name=abc,def)
            for key, value in request.query_params.items():
                if ',' in value:
                    values = value.split(',')
                    queryset = queryset.filter(**{f"{key}__in": values})
                else:
                    queryset = queryset.filter(**{key: value})

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = self.serializer_class(queryset, many=True)
            return Response(serialized_data.data)

        except Exception as e:
            return Response({
                'message': f'Error occurred: {str(e)}',
                'status': 400
            })
