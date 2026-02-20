



from uuid import UUID
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import EventCategory
from ..serializers import EventCategorySerializer
class EventCategoryView(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    # permission_classes = []
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    def list(self, request):
        raw_ids = [
            "1cb6a4e7-0491-4516-b096-4c80b8f3caa7",
            "7426b52b-4046-4fe8-9d04-278a9d3562f8",
            "d8d437e8-1a6c-49ea-8cb6-55398bfd0989",
            "a03301df-2f2b-47de-a23d-98b186ed7aca",
            "5ae77981-ce01-432c-bdd9-1e9cf815f8b2",
            "83d00234-ebba-4aea-b896-0c8dbe6d5932",
            "a667b7f9-0a23-4bb6-bcd3-f042cb7a9060",
            "c18ec6e7-938c-42c9-8967-14c950167a4e",
            "1e3034dc-4661-4fdd-86a5-e3ee90ac3c49",
        ]
        try:
            # Convert the raw_ids to UUID objects
            ordered_uuids = [UUID(uid) for uid in raw_ids]
        except ValueError:
            return Response({"error": "Invalid UUID in ordering list."}, status=400)
        # Filter the queryset using UUIDs in the raw_ids
        queryset = EventCategory.objects.filter(_id__in=ordered_uuids)  # Use `_id` or `id` as per your model field
        # Ensure the queryset is not empty
        if not queryset.exists():
            return Response({'message': 'No matching EventCategories found', 'status': 404})
        # Create a mapping from the `_id` field to the model instance (for easy ordering)
        uuid_to_obj = {str(obj._id): obj for obj in queryset}  # Ensure you're using `_id` or `id` depending on your model
        # Order the queryset according to the original list of raw_ids
        ordered_queryset = [uuid_to_obj.get(str(uid)) for uid in ordered_uuids if str(uid) in uuid_to_obj]
        # Check if we found any records to return
        if not ordered_queryset:
            return Response({'message': 'No matching EventCategories found', 'status': 404})
        # Serialize and return the ordered queryset
        serializer = self.get_serializer(ordered_queryset, many=True)
        return Response(serializer.data)




