# views.py
from rest_framework import viewsets, permissions
from ..models import VillageDevelopmentFacility
from ..serializers import VillageDevelopmentFacilitySerializer
from ..utils import save_image_to_azure
from rest_framework import viewsets, status
from rest_framework.response import Response

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