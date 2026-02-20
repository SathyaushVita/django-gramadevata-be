from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from ..models import TempleFestival
from ..serializers import TempleFestivalSerializer
from ..utils import save_image_to_azure  # Ensure this is properly imported

class TempleFestivalViewSet(viewsets.ModelViewSet):
    queryset = TempleFestival.objects.all()
    serializer_class = TempleFestivalSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == 'GET':
            filter_kwargs = {'status': 'ACTIVE'}
            for key, value in self.request.query_params.items():
                filter_kwargs[key] = value
            return TempleFestival.objects.filter(**filter_kwargs)
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.method == 'GET' and instance.status != 'ACTIVE':
            return Response({
                'message': 'Data not found',
                'status': 404
            })
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set image_location to "null"
            request.data['image_location'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []
            if image_locations and "null" not in image_locations:
                entity_type = "temple_festival"

                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)

            if saved_locations:
                serializer.instance.image_location = saved_locations
                serializer.instance.save()

            created_at = timezone.now()

            # Send email to admin
            send_mail(
                'New Temple Festival Added',
                f'User ID: {request.user.id}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Festival ID: {serializer.instance._id}\n'
                f'Festival Name: {serializer.instance.name}',
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
