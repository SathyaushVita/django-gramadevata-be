# from ..models import State
# from ..serializers import StateSeerializer
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from rest_framework .response import Response
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator



# class StateViews(viewsets.ModelViewSet):
#     queryset = State.objects.all()
#     serializer_class = StateSeerializer

#     @method_decorator(cache_page(60 * 5))  # cache for 5 minutes
#     def list(self, request):
#         filter_kwargs = {}

#         for key, value in request.query_params.items():
#             filter_kwargs[key] = value

#         try:
#             queryset = State.objects.filter(**filter_kwargs)

#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serializer = StateSeerializer(queryset, many=True)
#             return Response(serializer.data)

#         except State.DoesNotExist:
#             return Response({
#                 'message': 'Objects not found',
#                 'status': 404
#             })






from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import State
from ..serializers import StateSeerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class StateViews(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSeerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params.dict()

        # pagination params remove
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
