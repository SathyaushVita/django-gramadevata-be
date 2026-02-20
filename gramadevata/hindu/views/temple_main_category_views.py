from rest_framework import viewsets
from rest_framework.response import Response

from ..models import TempleMainCategory
from ..serializers import TempleMainCategorySerializer
class TempleMainCategoryViewSet(viewsets.ModelViewSet):
    queryset = TempleMainCategory.objects.all()
    serializer_class = TempleMainCategorySerializer

    def list(self, request, *args, **kwargs):
        main_categories_id = [
            "e9e8933f-81ee-42bd-9b6d-e923d30d2e5b",
            "64dece57-7b94-4eb1-b31c-884bfa57fcce",
            "ed4b72fd-5dd7-4749-9852-a4483899642b",
            "56ee646b-8370-4129-84f5-22af7ed538e5"
        ]

        filter_kwargs = dict(request.query_params.items())

        if filter_kwargs:
            queryset = self.queryset.filter(**filter_kwargs, _id__in=main_categories_id)
        else:
            queryset = self.queryset.filter(_id__in=main_categories_id)

        # Preserve the order from main_categories_id
        id_to_obj = {str(obj._id): obj for obj in queryset}
        ordered_queryset = [id_to_obj[_id] for _id in main_categories_id if _id in id_to_obj]

        if not ordered_queryset:
            return Response({
                'message': 'No matching data found',
                'status': 404
            }, status=404)

        serializer = self.get_serializer(ordered_queryset, many=True)
        return Response(serializer.data)
