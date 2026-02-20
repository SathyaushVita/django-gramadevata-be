from rest_framework import viewsets
from ..models import PujariSubCategory
from ..serializers import PujariSubCategorySerializer
from uuid import UUID

class PujariSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = PujariSubCategory.objects.all()
    serializer_class = PujariSubCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_kwargs = {}

        # Handle multiple category filtering
        category_ids = self.request.query_params.get('category')
        if category_ids:
            try:
                category_id_list = [UUID(cid.strip()) for cid in category_ids.split(',')]
                filter_kwargs['category__in'] = category_id_list
            except ValueError:
                return queryset.none()

        # Handle multiple _id filtering
        ids_param = self.request.query_params.get('_id')
        if ids_param:
            try:
                id_list = [UUID(i.strip()) for i in ids_param.split(',')]
                filter_kwargs['_id__in'] = id_list
            except ValueError:
                return queryset.none()

        # Handle other single-value filters dynamically
        for key, value in self.request.query_params.items():
            if key not in ['category', '_id']:  # already handled
                filter_kwargs[key] = value

        return queryset.filter(**filter_kwargs)
