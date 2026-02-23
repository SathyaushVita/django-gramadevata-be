from datetime import datetime
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from ..models import PoliceStation
from ..serializers import PoliceStationSerializer,InactivePoliceStationSerializer
from ..utils import save_image_to_azure 


class PoliceStationView(viewsets.ModelViewSet):
    queryset = PoliceStation.objects.all()
    serializer_class = PoliceStationSerializer
    # permission_classes = [IsAuthenticated]  

    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        filter_kwargs['status'] = 'ACTIVE'

        queryset = PoliceStation.objects.filter(**filter_kwargs)
        if not queryset.exists():
            return Response({'message': 'Data not found', 'status': 404})

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        try:
            # Extract image_location from request data
            image_locations = request.data.get('image_location', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set image_location to "null" for serializer
            request.data['image_location'] = "null"

            # Check and ensure created_at is a datetime object
            created_at_str = request.data.get('created_at', None)
            if created_at_str:
                try:
                    # If created_at is a string, convert it to datetime
                    created_at = datetime.fromisoformat(created_at_str)  # ISO 8601 format
                    request.data['created_at'] = created_at
                except ValueError:
                    # If conversion fails, use current time
                    request.data['created_at'] = timezone.now()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []
            entity_type = "policestation"

            # Process each image location
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

            user_id = request.user.id if request.user.is_authenticated else "Anonymous"
            created_at = serializer.instance.created_at

            # Ensure created_at is a datetime object and convert if it's a string
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at)
                except ValueError:
                    created_at = timezone.now()

            from django.utils.timezone import localtime
            created_time_str = localtime(created_at).strftime("%Y-%m-%d %H:%M:%S")

            send_mail(
                'New PoliceStation Added',
                f'User ID: {user_id}\n'
                f'Created Time: {created_time_str}\n'
                f'policestation ID: {serializer.instance._id}\n'
                f'policestation Name: {serializer.instance.name}',
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
            instance = PoliceStation.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except PoliceStation.DoesNotExist:
            return Response({
                "message": "police station not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)










class InactivePoliceStationAPIView(APIView):

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        queryset = PoliceStation.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(village_id__name__icontains=search_query) 
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactivePoliceStationSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_police_stations": serializer.data
        }, status=status.HTTP_200_OK)