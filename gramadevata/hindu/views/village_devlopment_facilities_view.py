from rest_framework import viewsets, permissions
from ..models import VillageDevelopmentFacility
from ..serializers import VillageDevelopmentFacilitySerializer,InactiveVillageDevelopmentFacilitySerializer
from ..utils import save_image_to_azure
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q



class VillageDevelopmentFacilityViewSet(viewsets.ModelViewSet):
    queryset = VillageDevelopmentFacility.objects.all()
    serializer_class = VillageDevelopmentFacilitySerializer

    def create(self, request, *args, **kwargs):
            try:
                # Extract image base64 list safely
                livelihood_images = request.data.get('primarysource_of_livelihood_image', [])
                if isinstance(livelihood_images, str):
                    livelihood_images = [livelihood_images]
                elif not isinstance(livelihood_images, list):
                    livelihood_images = []

                # Temporarily remove from request for serializer validation
                request_data = request.data.copy()
                request_data['primarysource_of_livelihood_image'] = []

                # Save initial object without images
                serializer = self.get_serializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # Upload images to Azure
                saved_images = []
                entity_type = "village_development_facilities"
                for image in livelihood_images:
                    if image and image.strip() and image != "null":
                        saved_path = save_image_to_azure(
                            image_data=image,
                            _id=serializer.instance._id,
                            name="primary_livelihood",
                            entity_type=entity_type
                        )
                        if saved_path:
                            saved_images.append(saved_path)

                # Update the model instance with image paths
                serializer.instance.primarysource_of_livelihood_image = saved_images
                serializer.instance.save()

                return Response(self.get_serializer(serializer.instance).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)










class InactiveVillageDevelopmentFacilityAPIView(APIView):
    """
    API to get only INACTIVE Village Development Facilities
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        queryset = VillageDevelopmentFacility.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        if search_query:
            queryset = queryset.filter(
                Q(village_id__name__icontains=search_query) |
                Q(bank_name__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveVillageDevelopmentFacilitySerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_village_development_facilities": serializer.data
        }, status=status.HTTP_200_OK)