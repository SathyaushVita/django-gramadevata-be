# views.py
from rest_framework import viewsets, permissions
from ..models import VillageCulturalProfile
from ..serializers import VillageCulturalProfileSerializer,InactiveVillageCulturalProfileSerializer
from ..utils import save_image_to_azure
from rest_framework import viewsets, status
from rest_framework.response import Response  
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q





class VillageCulturalProfileViewSet(viewsets.ModelViewSet):
    queryset = VillageCulturalProfile.objects.all()
    serializer_class = VillageCulturalProfileSerializer



    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()

            # Extract and store raw image data (base64 lists) for each field
            religios_beliefs_image = data.pop('religios_beliefs_image', [])
            traditional_food_image = data.pop('traditional_food_image', [])
            traditional_dress_image = data.pop('traditional_dress_image', [])
            traditional_ornaments_image = data.pop('traditional_ornaments_image', [])
            festivals_image = data.pop('festivals_image', [])
            art_forms_practiced_image = data.pop('art_forms_practiced_image', [])

            # Ensure each field is a list (even if a single string is passed)
            def ensure_list(value):
                return value if isinstance(value, list) else [value]

            religios_beliefs_image = ensure_list(religios_beliefs_image)
            traditional_food_image = ensure_list(traditional_food_image)
            traditional_dress_image = ensure_list(traditional_dress_image)
            traditional_ornaments_image = ensure_list(traditional_ornaments_image)
            festivals_image = ensure_list(festivals_image)
            art_forms_practiced_image = ensure_list(art_forms_practiced_image)

            # Set image fields to None temporarily
            image_fields = [
                'religios_beliefs_image', 'traditional_food_image', 'traditional_dress_image',
                'traditional_ornaments_image', 'festivals_image', 'art_forms_practiced_image'
            ]
            for field in image_fields:
                data[field] = None  # ✅ FIXED: use None instead of "null"

            # Validate and create instance
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            instance = serializer.instance
            entity_type = "village_culture"

            # Save images and update instance fields
            instance.religios_beliefs_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in religios_beliefs_image
            ]
            instance.traditional_food_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in traditional_food_image
            ]
            instance.traditional_dress_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in traditional_dress_image
            ]
            instance.traditional_ornaments_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in traditional_ornaments_image
            ]
            instance.festivals_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in festivals_image
            ]
            instance.art_forms_practiced_image = [
                save_image_to_azure(img, instance._id, instance.famous_for, entity_type)
                for img in art_forms_practiced_image
            ]

            instance.save()

            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)













class InactiveVillageCulturalProfileAPIView(APIView):
    """
    API to get only INACTIVE Village Cultural Profiles
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE cultural profiles
        queryset = VillageCulturalProfile.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by village name
        if search_query:
            queryset = queryset.filter(
                Q(village_id__name__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveVillageCulturalProfileSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_village_cultural_profiles": serializer.data
        }, status=status.HTTP_200_OK)