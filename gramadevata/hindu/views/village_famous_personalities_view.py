# views.py
from rest_framework import viewsets, status
from ..models import VillageFamousPersonality
from ..serializers import VillageFamousPersonalitySerializer
from ..utils import save_image_to_azure 
from django.conf import settings
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail



class VillageFamousPersonalityViewSet(viewsets.ModelViewSet):
    queryset = VillageFamousPersonality.objects.all()
    serializer_class = VillageFamousPersonalitySerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]





    def create(self, request, *args, **kwargs):
            try:
                # Handle image upload
                person_images = request.data.get('person_image', [])
                if not isinstance(person_images, list):
                    person_images = [person_images]
                request.data['person_image'] = "null"

                # Save main personality data
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                saved_images = []
                entity_type = "famous_personality"

                # Save images to Azure
                if person_images and "null" not in person_images:
                    for image in person_images:
                        if image and image != "null":
                            saved_location = save_image_to_azure(
                                image,
                                serializer.instance._id,
                                serializer.instance.person_name or "Unknown",
                                entity_type
                            )
                            if saved_location:
                                saved_images.append(saved_location)

                # Update model with saved image paths
                if saved_images:
                    serializer.instance.person_image = saved_images
                    serializer.instance.save()

                # Send Email Notification
                created_at = timezone.now()
                send_mail(
                    'New Village Famous Personality Added',
                    f'User ID: {request.user.id}\n'
                    f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                    f'Personality ID: {serializer.instance._id}\n'
                    f'Person Name: {serializer.instance.person_name}',
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
                instance = self.get_object()
            except VillageFamousPersonality.DoesNotExist:
                return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def update(self, request, pk=None):
            try:
                instance = self.get_object()

                # Extract person_image from request data
                person_images = request.data.get('person_image', [])
                if not isinstance(person_images, list):
                    person_images = [person_images]

                # Temporarily set person_image to "null"
                request.data['person_image'] = "null"

                # Serialize and update the instance
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                updated_instance = serializer.save()

                saved_images = []
                entity_type = "famous_personality"

                if person_images and "null" not in person_images:
                    for image in person_images:
                        if image and image != "null":
                            saved_location = save_image_to_azure(
                                image,
                                updated_instance._id,
                                updated_instance.person_name or "Unknown",
                                entity_type
                            )
                            if saved_location:
                                saved_images.append(saved_location)

                if saved_images:
                    updated_instance.person_image = saved_images
                    updated_instance.save()

                updated_time = timezone.now()

                # Send email notification
                send_mail(
                    'Village Famous Personality Updated',
                    f'User ID: {request.user.id}\n'
                    f'Full Name: {request.user.get_full_name()}\n'
                    f'Updated Time: {updated_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                    f'Personality ID: {updated_instance._id}\n'
                    f'Person Name: {updated_instance.person_name}',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )

                return Response({
                    "message": "updated successfully",
                    "data": self.get_serializer(updated_instance).data
                })

            except Exception as e:
                return Response({
                    "message": "An error occurred.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)