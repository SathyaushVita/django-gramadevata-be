
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from ..models import PrayersAndBenefits
from ..serializers import PrayersAndBenefitsSerializer

class PrayersAndBenefitsViewSet(viewsets.ModelViewSet):
    queryset = PrayersAndBenefits.objects.all()
    serializer_class = PrayersAndBenefitsSerializer

    def get_queryset(self):
        filter_kwargs = {'status': 'ACTIVE'}
        for key, value in self.request.query_params.items():
            filter_kwargs[key] = value
        return PrayersAndBenefits.objects.filter(**filter_kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'ACTIVE':
            return Response({'message': 'Data not found', 'status': 404})
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=request.user)

            created_at = timezone.now()
            if request.user and request.user.is_authenticated:
                send_mail(
                    'New Prayer and Benefit Added',
                    f'User ID: {request.user.id}\n'
                    f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                    f'Temple ID: {serializer.instance.temple_id_id}\n'
                    f'Entry ID: {serializer.instance._id}',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
