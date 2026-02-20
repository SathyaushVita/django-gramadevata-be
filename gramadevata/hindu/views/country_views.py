from ..serializers import CountrySerializer,CountrySerializer1
from ..models import Country
from rest_framework import viewsets
from rest_framework .response import Response
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# class CountryViews(viewsets.ModelViewSet):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer

#     @method_decorator(cache_page(60 * 5))  # cache for 5 minutes
#     def list(self, request):
#         filter_kwargs = {}

#         for key, value in request.query_params.items():
#             filter_kwargs[key] = value

#         try:
#             queryset = Country.objects.filter(**filter_kwargs)

#             if not queryset.exists():
#                 return Response({
#                     'message': 'Data not found',
#                     'status': 404
#                 })

#             serializer = CountrySerializer1(queryset, many=True)
#             return Response(serializer.data)

#         except Country.DoesNotExist:
#             return Response({
#                 'message': 'Objects not found',
#                 'status': 404
#             })















from django.db.models import Exists, OuterRef
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from ..models import Country, Temple, Event, Goshala,WelfareHomes,TempleNearbyTourismPlace,NearbyHospital,VeterinaryHospital,BloodBank,TempleNearbyHotel,TempleNearbyRestaurant,PoojaStore,TourOperator
from ..serializers import CountrySerializer1
from django.db.models import Exists, OuterRef, Q

from rest_framework import viewsets, status








@method_decorator(cache_page(60 * 5), name="dispatch")
class CountryViews(viewsets.ModelViewSet):
    serializer_class = CountrySerializer1
    http_method_names = ["get"]

    def get_queryset(self):
        page_type = self.request.query_params.get("page_type")
        category_id = self.request.query_params.get("category_id")

        queryset = Country.objects.all()

        # ==================================================
        # CASE 1: ONLY category_id (NO page_type)
        # ==================================================
        if category_id and not page_type:
            queryset = queryset.filter(
                Q(
                    Exists(
                        Temple.objects.filter(
                            status="ACTIVE",
                            category_id=category_id,
                        ).filter(
                            Q(country=OuterRef("pk")) |
                            Q(object_id__block__district__state__country=OuterRef("pk"))
                        )
                    )
                )
                |
                Q(
                    Exists(
                        Goshala.objects.filter(
                            status="ACTIVE",
                            category_id=category_id,
                        ).filter(
                            Q(country=OuterRef("pk")) |
                            Q(object_id__block__district__state__country=OuterRef("pk"))
                        )
                    )
                )
                |
                Q(
                    Exists(
                        Event.objects.filter(
                            status="ACTIVE",
                            category_id=category_id,
                        ).filter(
                            Q(country=OuterRef("pk")) |
                            Q(object_id__block__district__state__country=OuterRef("pk"))
                        )
                    )
                )
                |
                Q(
                    Exists(
                        WelfareHomes.objects.filter(
                            status="ACTIVE",
                            category_id=category_id,
                            village_id__block__district__state__country=OuterRef("pk"),
                        )
                    )
                )
            )

        # ==================================================
        # TEMPLE
        # ==================================================
        elif page_type == "temple":
            qs = Temple.objects.filter(status="ACTIVE")
            if category_id:
                qs = qs.filter(category_id=category_id)

            queryset = queryset.filter(
                Exists(
                    qs.filter(
                        Q(country=OuterRef("pk")) |
                        Q(object_id__block__district__state__country=OuterRef("pk"))
                    )
                )
            )

        # ==================================================
        # GOSHALA
        # ==================================================
        elif page_type == "goshala":
            qs = Goshala.objects.filter(status="ACTIVE")
            if category_id:
                qs = qs.filter(category_id=category_id)

            queryset = queryset.filter(
                Exists(
                    qs.filter(
                        Q(country=OuterRef("pk")) |
                        Q(object_id__block__district__state__country=OuterRef("pk"))
                    )
                )
            )

        # ==================================================
        # EVENT
        # ==================================================
        elif page_type == "event":
            qs = Event.objects.filter(status="ACTIVE")
            if category_id:
                qs = qs.filter(category_id=category_id)

            queryset = queryset.filter(
                Exists(
                    qs.filter(
                        Q(country=OuterRef("pk")) |
                        Q(object_id__block__district__state__country=OuterRef("pk"))
                    )
                )
            )

        # ==================================================
        # WELFARE HOMES
        # ==================================================
        elif page_type == "welfare":
            qs = WelfareHomes.objects.filter(status="ACTIVE")
            if category_id:
                qs = qs.filter(category_id=category_id)

            queryset = queryset.filter(
                Exists(
                    qs.filter(
                        village_id__block__district__state__country=OuterRef("pk")
                    )
                )
            )

        # ==================================================
        # TOURISM PLACES
        # ==================================================
        elif page_type == "tourism":
            queryset = queryset.filter(
                Exists(
                    TempleNearbyTourismPlace.objects.filter(status="ACTIVE").filter(
                        Q(country=OuterRef("pk")) |
                        Q(village_id__block__district__state__country=OuterRef("pk"))
                    )
                )
            )

        # ==================================================
        # NEARBY HOSPITAL
        # ==================================================
        elif page_type == "hospital":
            queryset = queryset.filter(
                Exists(
                    NearbyHospital.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # VETERINARY HOSPITAL
        # ==================================================
        elif page_type == "veterinary_hospital":
            queryset = queryset.filter(
                Exists(
                    VeterinaryHospital.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # BLOOD BANK
        # ==================================================
        elif page_type == "blood_bank":
            queryset = queryset.filter(
                Exists(
                    BloodBank.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # TEMPLE NEARBY HOTEL
        # ==================================================
        elif page_type == "hotel":
            queryset = queryset.filter(
                Exists(
                    TempleNearbyHotel.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # TEMPLE NEARBY RESTAURANT
        # ==================================================
        elif page_type == "restaurant":
            queryset = queryset.filter(
                Exists(
                    TempleNearbyRestaurant.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # POOJA STORE
        # ==================================================
        elif page_type == "pooja_store":
            queryset = queryset.filter(
                Exists(
                    PoojaStore.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        # ==================================================
        # TOUR OPERATOR
        # ==================================================
        elif page_type == "tour_operator":
            queryset = queryset.filter(
                Exists(
                    TourOperator.objects.filter(
                        status="ACTIVE",
                        village_id__block__district__state__country=OuterRef("pk"),
                    )
                )
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {"message": "Data not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)











# @method_decorator(cache_page(60 * 5), name="dispatch")
# class CountryViews(viewsets.ModelViewSet):
#     serializer_class = CountrySerializer1
#     http_method_names = ["get"]

#     def get_queryset(self):
#         page_type = self.request.query_params.get("page_type")
#         queryset = Country.objects.all()

#         # ==================================================
#         # TEMPLE
#         # ==================================================
#         if page_type == "temple":
#             queryset = queryset.filter(
#                 Exists(
#                     Temple.objects.filter(status="ACTIVE").filter(
#                         Q(country=OuterRef("pk")) |
#                         Q(object_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # GOSHALA
#         # ==================================================
#         elif page_type == "goshala":
#             queryset = queryset.filter(
#                 Exists(
#                     Goshala.objects.filter(status="ACTIVE").filter(
#                         Q(country=OuterRef("pk")) |
#                         Q(object_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # EVENT
#         # ==================================================
#         elif page_type == "event":
#             queryset = queryset.filter(
#                 Exists(
#                     Event.objects.filter(status="ACTIVE").filter(
#                         Q(country=OuterRef("pk")) |
#                         Q(object_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # TOURISM PLACES
#         # ==================================================
#         elif page_type == "tourism":
#             queryset = queryset.filter(
#                 Exists(
#                     TempleNearbyTourismPlace.objects.filter(status="ACTIVE").filter(
#                         Q(country=OuterRef("pk")) |
#                         Q(village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # WELFARE HOMES
#         # ==================================================
#         elif page_type == "welfare":
#             queryset = queryset.filter(
#                 Exists(
#                     WelfareHomes.objects.filter(
#                         status="ACTIVE",
#                         village_id__block__district__state__country=OuterRef("pk")
#                     )
#                 )
#             )

#         # ==================================================
#         # NEARBY HOSPITAL
#         # ==================================================
#         elif page_type == "hospital":
#             queryset = queryset.filter(
#                 Exists(
#                     NearbyHospital.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # VETERINARY HOSPITAL
#         # ==================================================
#         elif page_type == "veterinary_hospital":
#             queryset = queryset.filter(
#                 Exists(
#                     VeterinaryHospital.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # BLOOD BANK
#         # ==================================================
#         elif page_type == "blood_bank":
#             queryset = queryset.filter(
#                 Exists(
#                     BloodBank.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk")) 
#                         # Q(temple_id__object_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # TEMPLE NEARBY HOTEL
#         # ==================================================
#         elif page_type == "hotel":
#             queryset = queryset.filter(
#                 Exists(
#                     TempleNearbyHotel.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk")) 
#                         # Q(temple_id__object_id__block__district__state__country=OuterRef("pk")) |
#                         # Q(event_id__village_id__block__district__state__country=OuterRef("pk")) |
#                         # Q(tourism_places__village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # TEMPLE NEARBY RESTAURANT
#         # ==================================================
#         elif page_type == "restaurant":
#             queryset = queryset.filter(
#                 Exists(
#                     TempleNearbyRestaurant.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk")) 
#                         # Q(temple_id__object_id__block__district__state__country=OuterRef("pk")) |
#                         # Q(event_id__village_id__block__district__state__country=OuterRef("pk")) |
#                         # Q(tourism_places__village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # POOJA STORE
#         # ==================================================
#         elif page_type == "pooja_store":
#             queryset = queryset.filter(
#                 Exists(
#                     PoojaStore.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk")) 
#                         # Q(temple_id__object_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         # ==================================================
#         # TOUR OPERATOR
#         # ==================================================
#         elif page_type == "tour_operator":
#             queryset = queryset.filter(
#                 Exists(
#                     TourOperator.objects.filter(status="ACTIVE").filter(
#                         Q(village_id__block__district__state__country=OuterRef("pk")) 
#                     #     Q(temple_id__object_id__block__district__state__country=OuterRef("pk")) |
#                     #     Q(event_id__village_id__block__district__state__country=OuterRef("pk"))
#                     )
#                 )
#             )

#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()

#         if not queryset.exists():
#             return Response(
#                 {"message": "Data not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

