

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
import base64
from ..models import Media
from ..serializers import MediaSerializer
from ..utils import save_video_to_azure  # Import function for saving videos

class MediaView(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer



    def get_queryset(self):
        # Apply status filter only for list and retrieve actions
        if self.action in ['list', 'retrieve']:
            return Media.objects.filter(status='ACTIVE')
        return Media.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # Fetch user
            register_instance = request.user if request.user.is_authenticated else None
            if not register_instance:
                return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # Handle multiple video uploads
            video_data_list = request.data.get("video", [])  # Expecting a list of base64 videos
            if not isinstance(video_data_list, list):
                video_data_list = [video_data_list]  # Convert to list if single video provided

            saved_video_paths = []

            # Process each video
            for video_data in video_data_list:
                if video_data:
                    saved_path = save_video_to_azure(video_data, register_instance.id, "media_video", "media")
                    if saved_path:
                        saved_video_paths.append(saved_path)

            # Set video paths to request data
            request.data["video"] = saved_video_paths

            # Serialize and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



    def update(self, request, pk=None):
        try:
            instance = self.get_object()

            # Fetch user
            register_instance = request.user if request.user.is_authenticated else None
            if not register_instance:
                return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            # Handle multiple video uploads
            video_data_list = request.data.get("video", [])
            if not isinstance(video_data_list, list):
                video_data_list = [video_data_list]

            saved_video_paths = []

            for video_data in video_data_list:
                if video_data and video_data != "null":
                    saved_path = save_video_to_azure(video_data, register_instance.id, "media_video", "media")
                    if saved_path:
                        saved_video_paths.append(saved_path)

            # Remove raw video data before validation
            data = request.data.copy()
            data.pop('video', None)

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            if saved_video_paths:
                updated_instance.video = saved_video_paths
                updated_instance.save()

            return Response({
                "message": "Updated successfully",
                "result": self.get_serializer(updated_instance).data
            })

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





    def list(self, request):
        # Filter only ACTIVE media
        queryset = self.queryset.filter(status='ACTIVE')

        # Apply pagination if needed
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Return all ACTIVE media without pagination
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





    def retrieve(self, request, pk=None):
        try:
            instance = Media.objects.get(_id=pk, status='ACTIVE')
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Media.DoesNotExist:
            return Response({
                "message": "Media not found",
                "status": 404
            }, status=status.HTTP_404_NOT_FOUND)

            
