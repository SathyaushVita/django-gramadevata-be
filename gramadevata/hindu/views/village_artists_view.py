from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from ..models import VillageArtist
from ..serializers import VillageArtistSerializer,InactiveVillageArtistSerializer
from ..utils import save_image_to_azure, save_video_to_azure, save_audio_to_azure
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
 

class VillageArtistViewSet(viewsets.ModelViewSet):
    queryset = VillageArtist.objects.all()
    serializer_class = VillageArtistSerializer

    def create(self, request, *args, **kwargs):
        try:
            # 1. Handle artist_image
            artist_images = request.data.get('artist_image', [])
            if not isinstance(artist_images, list):
                artist_images = [artist_images]
            request.data['artist_image'] = "null"

            # 2. Handle traditional_occupation_pics
            occupation_images = request.data.get('traditional_occupation_pics', [])
            if not isinstance(occupation_images, list):
                occupation_images = [occupation_images]
            request.data['traditional_occupation_pics'] = "null"

            # 3. Handle traditional_occupation_video
            occupation_videos = request.data.get('traditional_occupation_video', [])
            if not isinstance(occupation_videos, list):
                occupation_videos = [occupation_videos]
            request.data['traditional_occupation_video'] = "null"

            # 4. Handle trained_under_pics
            trained_pics = request.data.get('trained_under_pics', [])
            if not isinstance(trained_pics, list):
                trained_pics = [trained_pics]
            request.data['trained_under_pics'] = "null"

            # 5. Handle audio_recordings
            audio_files = request.data.get('audio_recordings', [])
            if not isinstance(audio_files, list):
                audio_files = [audio_files]
            request.data['audio_recordings'] = "null"

            # Save the main VillageArtist data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Prepare to save each media type
            saved_artist_images = []
            saved_occupation_images = []
            saved_occupation_videos = []
            saved_trained_images = []
            saved_audio_files = []

            entity_type = "village_artist"
            artist_name = serializer.instance.artist_name or "Unknown"

            # Save artist_image
            if artist_images and "null" not in artist_images:
                for image in artist_images:
                    if image and image != "null":
                        saved_location = save_image_to_azure(image, serializer.instance._id, artist_name, f"{entity_type}/artist_image")
                        if saved_location:
                            saved_artist_images.append(saved_location)

            # Save traditional_occupation_pics
            if occupation_images and "null" not in occupation_images:
                for image in occupation_images:
                    if image and image != "null":
                        saved_location = save_image_to_azure(image, serializer.instance._id, artist_name, f"{entity_type}/traditional_occupation_pics")
                        if saved_location:
                            saved_occupation_images.append(saved_location)

            # Save traditional_occupation_video
            if occupation_videos and "null" not in occupation_videos:
                for video in occupation_videos:
                    if video and video != "null":
                        saved_location = save_video_to_azure(video, serializer.instance._id, artist_name, f"{entity_type}/traditional_occupation_video")
                        if saved_location:
                            saved_occupation_videos.append(saved_location)

            # Save trained_under_pics
            if trained_pics and "null" not in trained_pics:
                for image in trained_pics:
                    if image and image != "null":
                        saved_location = save_image_to_azure(image, serializer.instance._id, artist_name, f"{entity_type}/trained_under_pics")
                        if saved_location:
                            saved_trained_images.append(saved_location)

            # Save audio_recordings
            if audio_files and "null" not in audio_files:
                for audio in audio_files:
                    if audio and audio != "null":
                        saved_location = save_audio_to_azure(audio, serializer.instance._id, artist_name, f"{entity_type}/audio_recordings")
                        if saved_location:
                            saved_audio_files.append(saved_location)

            # Update model with saved media
            if saved_artist_images:
                serializer.instance.artist_image = saved_artist_images
            if saved_occupation_images:
                serializer.instance.traditional_occupation_pics = saved_occupation_images
            if saved_occupation_videos:
                serializer.instance.traditional_occupation_video = saved_occupation_videos
            if saved_trained_images:
                serializer.instance.trained_under_pics = saved_trained_images
            if saved_audio_files:
                serializer.instance.audio_recordings = saved_audio_files

            if any([saved_artist_images, saved_occupation_images, saved_occupation_videos, saved_trained_images, saved_audio_files]):
                serializer.instance.save()

            # Send email notification
            created_at = timezone.now()
            send_mail(
                'New Village Artist Added',
                f'User ID: {request.user.id}\n'
                # f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Artist ID: {serializer.instance._id}\n'
                f'Artist Name: {serializer.instance.artist_name}',
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









class InactiveVillageArtistAPIView(APIView):
    """
    API to get only INACTIVE Village Artists
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE artists
        queryset = VillageArtist.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by artist_name or village name
        if search_query:
            queryset = queryset.filter(
                Q(artist_name__icontains=search_query) |
                Q(village_id__name__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveVillageArtistSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_village_artists": serializer.data
        }, status=status.HTTP_200_OK)