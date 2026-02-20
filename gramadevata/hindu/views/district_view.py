# from rest_framework import viewsets
# from ..models import District
# from ..serializers import DistrictSerializer
# from rest_framework .response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator



# class DistrictVIew(viewsets.ModelViewSet):
#     queryset = District.objects.all()
#     serializer_class = DistrictSerializer

#     @method_decorator(cache_page(60 * 5))  # cache for 5 minutes
#     def list(self, request):
#         filter_kwargs = {}

#         for key, value in request.query_params.items():
#             filter_kwargs[key] = value

#         try:
#             queryset = District.objects.filter(**filter_kwargs)

#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serializer = DistrictSerializer(queryset, many=True)
#             return Response(serializer.data)

#         except District.DoesNotExist:
#             return Response({
#                 'message': 'Objects not found',
#                 'status': 404
#             })









from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import District
from ..serializers import DistrictSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class DistrictVIew(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

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
