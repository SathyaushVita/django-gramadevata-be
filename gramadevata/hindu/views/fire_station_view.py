from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from ..models import FireStation
from ..serializers import FireStationSerializer
from ..utils import save_image_to_azure  

class FireStationView(viewsets.ModelViewSet):
    queryset = FireStation.objects.all()
    serializer_class = FireStationSerializer
    # permission_classes = [] 
    def list(self, request):
        filter_kwargs = {}

        # Add query params to filter
        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        # Always filter by status='ACTIVE' in GET requests
        filter_kwargs['status'] = 'ACTIVE'

        try:
            queryset = FireStation.objects.filter(**filter_kwargs)

            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            serialized_data = FireStationSerializer(queryset, many=True)
            return Response(serialized_data.data)
 
        except FireStation.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })

    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            request.data['image_location'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []  

            if image_locations and "null" not in image_locations:
                entity_type = "firestation"

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
            user_id = request.user.id if request.user.is_authenticated else "Anonymous"

            send_mail(
                'New Firestation Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Firestation ID: {serializer.instance._id}\n'
                f'Firestation Name: {serializer.instance.name}',
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





    def retrieve(self, request, pk=None):
        try:
            instance = FireStation.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FireStation.DoesNotExist:
            return Response({
                "message": "firestation not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)
