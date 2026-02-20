# views.py
from rest_framework import viewsets, permissions
from ..models import VillageMarket
from ..serializers import VillageMarketSerializer
from ..utils import save_image_to_azure
from rest_framework import viewsets, status
from rest_framework.response import Response

class VillageMarketViewSet(viewsets.ModelViewSet):
    queryset = VillageMarket.objects.all()
    serializer_class = VillageMarketSerializer

    def create(self, request, *args, **kwargs):
            try:
                # Extract image base64 list safely
                image_location = request.data.get('image_location', [])
                if isinstance(image_location, str):
                    image_location = [image_location]
                elif not isinstance(image_location, list):
                    image_location = []

                # Temporarily remove from request for serializer validation
                request_data = request.data.copy()
                request_data['image_location'] = []

                # Save initial object without images
                serializer = self.get_serializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # Upload images to Azure
                saved_images = []
                entity_type = "village-market"
                for image in image_location:
                    if image and image.strip() and image != "null":
                        saved_path = save_image_to_azure(
                            image_data=image,
                            _id=serializer.instance._id,
                            name="image_location",
                            entity_type=entity_type
                        )
                        if saved_path:
                            saved_images.append(saved_path)

                # Update the model instance with image paths
                serializer.instance.image_location = saved_images
                serializer.instance.save()

                return Response(self.get_serializer(serializer.instance).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)