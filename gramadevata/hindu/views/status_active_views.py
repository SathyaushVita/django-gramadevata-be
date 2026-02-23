from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import BloodBank, VillageBank, Accommodation
from ..enums import EntityStatus

from ..serializers import (
    BloodBankSerializer,
    VillageBankSerializer,
    AccommodationSerializer
)


class UniversalActivateAPIView(APIView):

    def put(self, request, id):

        models_with_serializers = [
            (BloodBank, BloodBankSerializer),
            (VillageBank, VillageBankSerializer),
            (Accommodation, AccommodationSerializer),
        ]

        for model, serializer_class in models_with_serializers:
            try:
                instance = model.objects.get(_id=id)

                instance.status = EntityStatus.ACTIVE.name
                instance.save()

                serializer = serializer_class(instance)

                return Response({
                    "message": f"{model.__name__} activated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            except model.DoesNotExist:
                continue

        return Response({
            "message": "ID not found in any model"
        }, status=status.HTTP_404_NOT_FOUND)