







from ..serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Case, When, IntegerField
from rest_framework.permissions import IsAuthenticated
from ..models import TempleCategory
class templeCategeoryview(viewsets.ModelViewSet):
    queryset = TempleCategory.objects.all()
    serializer_class = TempleCategeorySerializer1
    # permission_classes = []
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    def list(self, request):
        filter_kwargs = {}
        for key, value in request.query_params.items():
            filter_kwargs[key] = value
        try:
            queryset = TempleCategory.objects.filter(**filter_kwargs)
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })
            # Annotate order by category_id
            queryset = queryset.annotate(
                order_category=Case(
                    When(_id="742ccfe6-d0b5-11ee-84bd-0242ac110002", then=0),
                    When(_id="742ecf7b-d0b5-11ee-84bd-0242ac110002", then=1),
                    When(_id="742c4b08-d0b5-11ee-84bd-0242ac110002", then=2),
                    When(_id="742c309e-d0b5-11ee-84bd-0242ac110002", then=3),
                    When(_id="742c043d-d0b5-11ee-84bd-0242ac110002", then=4),
                    When(_id="405033fe-fb78-49e0-aef9-35172863466c", then=5),
                    When(_id="11633522-2084-4f76-b360-0a0038c3f285", then=6),
                    When(_id="743339d5-d0b5-11ee-84bd-0242ac110002", then=7),
                    When(_id="74333d89-d0b5-11ee-84bd-0242ac110002", then=8),
                    When(_id="74333f6a-d0b5-11ee-84bd-0242ac110002", then=9),
                    When(_id="72524742-6e3a-4c2a-b4d4-4a0a68b5faa7", then=10),
                    When(_id="957b393b-2198-4e3f-a7a5-61a1b1b9652b",then=11),
                    When(_id="742f645c-d0b5-11ee-84bd-0242ac110002", then=12),
                    When(_id="74343760-d0b5-11ee-84bd-0242ac110002", then=13),
                    # When(_id="742ccfe6-d0b5-11ee-84bd-0242ac110002", then=13),
                    When(_id="742f66d4-d0b5-11ee-84bd-0242ac110002", then=14),
                    When(_id="742ed15f-d0b5-11ee-84bd-0242ac110002", then=15),
                    When(_id="74353e76-d0b5-11ee-84bd-0242ac110002", then=16),
                    When(_id="74334755-d0b5-11ee-84bd-0242ac110002", then=17),
                    When(_id="742fb823-d0b5-11ee-84bd-0242ac110002", then=18),
                    When(_id="7434333a-d0b5-11ee-84bd-0242ac110002", then=19),
                    When(_id="7433a0e7-d0b5-11ee-84bd-0242ac110002", then=20),
                    When(_id="74344055-d0b5-11ee-84bd-0242ac110002", then=21),
                    When(_id="742ecbf6-d0b5-11ee-84bd-0242ac110002", then=22),
                    When(_id="742e85ad-d0b5-11ee-84bd-0242ac110002", then=23),
                    When(_id="74345ef3-d0b5-11ee-84bd-0242ac110002", then=24),
                    When(_id="74353c0d-d0b5-11ee-84bd-0242ac110002", then=25),
                    When(_id="742ed999-d0b5-11ee-84bd-0242ac110002", then=26),
                    When(_id="742b10a6-d0b5-11ee-84bd-0242ac110002", then=27),
                    When(_id="742da6dc-d0b5-11ee-84bd-0242ac110002", then=28),
                    When(_id="742f57d9-d0b5-11ee-84bd-0242ac110002", then=29),
                    When(_id="74344b60-d0b5-11ee-84bd-0242ac110002", then=30),
                    When(_id="742c8632-d0b5-11ee-84bd-0242ac110002", then=31),
                    When(_id="742ee33e-d0b5-11ee-84bd-0242ac110002", then=32),
                    When(_id="742cc4f8-d0b5-11ee-84bd-0242ac110002", then=33),
                    When(_id="742c5302-d0b5-11ee-84bd-0242ac110002", then=34),
                    When(_id="742da3d3-d0b5-11ee-84bd-0242ac110002", then=35),
                    When(_id="742f52be-d0b5-11ee-84bd-0242ac110002", then=36),
                    When(_id="74339dc3-d0b5-11ee-84bd-0242ac110002", then=37),
                    When(_id="743525d3-d0b5-11ee-84bd-0242ac110002", then=38),
                    When(_id="742f2965-d0b5-11ee-84bd-0242ac110002", then=39),
                    When(_id="742c0c1b-d0b5-11ee-84bd-0242ac110002", then=40),
                    When(_id="742c1781-d0b5-11ee-84bd-0242ac110002", then=41),
                    When(_id="742ebd7b-d0b5-11ee-84bd-0242ac110002", then=42),
                    When(_id="fee05763-b9b1-49d5-8423-b385625045ff", then=43),
                    When(_id="743340c9-d0b5-11ee-84bd-0242ac110002", then=44),
                    When(_id="a19958cc-86c2-44fc-a8f2-35c54208fae5", then=45),
                    When(_id="742fc433-d0b5-11ee-84bd-0242ac110002", then=46),
                    When(_id="05dd3bfa-8f5a-49f7-83de-520a3b1c012d", then=47),
                    When(_id="4117b4f9-f202-4b10-a637-50fc5151a0e4", then=48),
                    When(_id="2257a2c4-73ac-49c1-ba3d-376c10b0c664", then=49),
                    When(_id="142a703b-e8ad-4550-b68a-6a0718b90922", then=50),
                    When(_id="49eabde2-ce67-426a-a0ad-e51849910401", then=51),
                    When(_id="d4f979f4-2f7a-4aab-9782-702b31a21087", then=52),
                    When(_id="742fc5ca-d0b5-11ee-84bd-0242ac110002", then=53),
                    When(_id="6af7ab24-9a0e-42cb-a57a-372bc62cd842", then=54),
                    default=55,
                    output_field=IntegerField()
                )
            ).order_by('order_category')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = TempleCategeorySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = TempleCategeorySerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'message': f'Error: {str(e)}',
                'status': 500
            })











