
from rest_framework import viewsets
from ..models import *
from rest_framework .response import Response
from ..serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.timesince import timesince
from ..enums import CommentStatus
from rest_framework.decorators import action
from rest_framework import status as drf_status




class CommentView(viewsets.ModelViewSet):
    queryset = CommentModel.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    

    def get_queryset(self):
        # Return only comments with status ACTIVE
        return CommentModel.objects.filter(status=CommentStatus.ACTIVE.value).order_by("-created_at")

    def perform_destroy(self, instance):
        # Instead of deleting the comment, update the status to INACTIVE
        instance.status = CommentStatus.INACTIVE.value
        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Comment marked as inactive."}, status=drf_status.HTTP_204_NO_CONTENT)

    # Optional: Define a custom action to handle manual deletion (if needed)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_as_inactive(self, request, pk=None):
        try:
            comment = self.get_object()
            comment.status = CommentStatus.INACTIVE.value
            comment.save()
            return Response({"detail": "Comment status updated to INACTIVE."}, status=drf_status.HTTP_200_OK)
        except CommentModel.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=drf_status.HTTP_404_NOT_FOUND)


    for comment in queryset:
        if comment.created_at:
            comment.posted_time_ago = f"{timesince(comment.created_at)} ago"
            comment.save()