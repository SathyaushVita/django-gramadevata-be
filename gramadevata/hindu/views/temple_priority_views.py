



from ..serializers import TemplePrioritySerializer
from ..models import TemplePriority
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Case, When, IntegerField

class TemplePriorityView(viewsets.ModelViewSet):
    queryset = TemplePriority.objects.all()

    serializer_class = TemplePrioritySerializer

    def get_queryset(self):
        priority_ids = [
            'b78ac071-d0b5-11ee-84bd-0242ac110002',
            'b78ac28e-d0b5-11ee-84bd-0242ac110002',
            '630f3239-f515-47fb-be8d-db727b9f2174',
            'd7df749f-97e8-4635-a211-371c44b3c31f',
        ]

        # Create a custom order using Case/When
        ordering = Case(
            *[When(_id=pk, then=pos) for pos, pk in enumerate(priority_ids)],
            output_field=IntegerField()
        )

        return TemplePriority.objects.filter(_id__in=priority_ids).order_by(ordering)
