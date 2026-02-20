from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Temple

class TempleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = Temple
        fields = {
            'category': ['exact'],
        }

    def filter_queryset(self, queryset):
        input_value = self.request.query_params.get('input_value')
        if input_value:
            queryset = queryset.filter(
                Q(object_id__block__district__state__country=input_value) |
                Q(object_id__block__district__state=input_value) |
                Q(object_id__block__district=input_value) |
                Q(object_id__block=input_value)
            )
        return queryset
