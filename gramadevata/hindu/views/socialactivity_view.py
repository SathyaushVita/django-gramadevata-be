
from rest_framework import viewsets
from ..models import SocialActivity
from ..serializers import SocialActivitySerializer

class SocialActivityViewSet(viewsets.ModelViewSet):
    queryset = SocialActivity.objects.all()
    serializer_class = SocialActivitySerializer

    def get_queryset(self):
        filter_kwargs = {'status': 'ACTIVE'}
        for key, value in self.request.query_params.items():
            filter_kwargs[key] = value
        return SocialActivity.objects.filter(**filter_kwargs)
