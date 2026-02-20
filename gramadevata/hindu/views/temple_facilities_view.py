
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from ..models import TempleFacilities
from ..serializers import TempleFacilitiesSerializer

class TempleFacilitiesViewSet(viewsets.ModelViewSet):
    queryset = TempleFacilities.objects.all()
    serializer_class = TempleFacilitiesSerializer

    def get_queryset(self):
        filter_kwargs = {'status': 'ACTIVE'}
        for key, value in self.request.query_params.items():
            filter_kwargs[key] = value
        return TempleFacilities.objects.filter(**filter_kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'ACTIVE':
            return Response({'message': 'Data not found', 'status': 404})
        return super().retrieve(request, *args, **kwargs)

