



from rest_framework import viewsets, status, serializers  
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from ..models import VisitTemple
from ..serializers import VisitTempleSerializer

class VisitTempleViewSet(viewsets.ModelViewSet):
    queryset = VisitTemple.objects.all()
    serializer_class = VisitTempleSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You must be logged in to add a visit.")

        temple_id = self.request.data.get('temple_id')
        event_id = self.request.data.get('event_id')
        goshala_id = self.request.data.get('goshala_id')

        # Check if the visit already exists
        if temple_id and VisitTemple.objects.filter(user_id=user, temple_id=temple_id).exists():
            raise serializers.ValidationError({"detail": "Already visited this temple."})

        if event_id and VisitTemple.objects.filter(user_id=user, event_id=event_id).exists():
            raise serializers.ValidationError({"detail": "Already visited this event."})

        if goshala_id and VisitTemple.objects.filter(user_id=user, goshala_id=goshala_id).exists():
            raise serializers.ValidationError({"detail": "Already visited this goshala."})

        serializer.save(user_id=user)
