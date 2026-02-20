# from rest_framework import viewsets
# from ..models import Block
# from ..serializers import BlockSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework .response import Response
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

# class BlockView(viewsets.ModelViewSet):
#     queryset = Block.objects.all()
#     serializer_class = BlockSerializer

#     @method_decorator(cache_page(60 * 5))  # cache for 5 minutes
#     def list(self, request):
#         filter_kwargs = {}

#         for key, value in request.query_params.items():
#             filter_kwargs[key] = value

#         try:
#             queryset = Block.objects.filter(**filter_kwargs)

#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serializer = BlockSerializer(queryset, many=True)
#             return Response(serializer.data)

#         except Block.DoesNotExist:
#             return Response({
#                 'message': 'Objects not found',
#                 'status': 404
#             })







from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import Block
from ..serializers import BlockSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class BlockView(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params.dict()

        # remove pagination params
        params.pop("page", None)
        params.pop("page_size", None)

        if params:
            queryset = queryset.filter(**params)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset:
            return Response(
                {"message": "Data not found", "status": 404},
                status=404
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
