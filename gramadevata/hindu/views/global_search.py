

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Value
from django.db.models.functions import Lower, Replace
from django.core.cache import cache
import hashlib

from ..models import (
    Village, Block, District, Temple,
    Event, TempleNearbyTourismPlace,
    Goshala, WelfareHomes, State
)

from ..serializers import (
    VillageSearch,
    BlockSearch,
    DistrictSearchSerializer,
    TempleSearch,
    EventSearch,
    TourismPlaceSearchSerializer,
    GoshalaSearch,
    WelfareHomesSearchSerializer,
    StateSearch
)

SEARCH_LIMIT = 3  # 🔥 small & fast


class GlobalSearchView(APIView):

    def normalize(self, text):
        return text.replace(" ", "").lower()

    def cache_key(self, search):
        return "gs:" + hashlib.md5(search.encode()).hexdigest()

    def get_match(self, queryset, search):
        return queryset.annotate(
            normalized_name=Lower(
                Replace(F("name"), Value(" "), Value(""))
            )
        ).filter(
            normalized_name__icontains=search
        )[:SEARCH_LIMIT]

    def get(self, request):
        search = request.query_params.get("search", "").strip()

        if not search:
            return Response({"message": "Search text is required"}, status=400)

        search = self.normalize(search)
        key = self.cache_key(search)

        # 🔥 REDIS HIT
        cached = cache.get(key)
        if cached:
            return Response(cached)

        data = []
        types = set()

        def append_results(queryset, serializer, type_name):
            for obj in queryset:
                item = serializer(obj).data
                item["type"] = type_name
                data.append(item)
                types.add(type_name)

        append_results(
            self.get_match(
                Village.objects.only("_id", "name"),
                search
            ),
            VillageSearch,
            "village"
        )

        append_results(
            self.get_match(
                Block.objects.only("_id", "name"),
                search
            ),
            BlockSearch,
            "block"
        )

        append_results(
            self.get_match(
                District.objects.only("_id", "name"),
                search
            ),
            DistrictSearchSerializer,
            "district"
        )

        append_results(
            self.get_match(
                Temple.objects.only("_id", "name"),
                search
            ),
            TempleSearch,
            "temple"
        )

        append_results(
            self.get_match(
                TempleNearbyTourismPlace.objects.only("_id", "name"),
                search
            ),
            TourismPlaceSearchSerializer,
            "tourism_place"
        )

        append_results(
            self.get_match(
                Event.objects.only("_id", "name"),
                search
            ),
            EventSearch,
            "event"
        )

        append_results(
            self.get_match(
                Goshala.objects.only("_id", "name"),
                search
            ),
            GoshalaSearch,
            "goshala"
        )

        append_results(
            self.get_match(
                WelfareHomes.objects.only("_id", "name"),
                search
            ),
            WelfareHomesSearchSerializer,
            "welfare_home"
        )

        append_results(
            self.get_match(
                State.objects.only("_id", "name"),
                search
            ),
            StateSearch,
            "state"
        )

        if not data:
            response = {"message": "No matching data found"}
            cache.set(key, response, timeout=60)  # small TTL
            return Response(response, status=404)

        response = {
            "type": list(types),
            "data": data
        }

        # 🔥 cache light response
        cache.set(key, response, timeout=120)  # 2 minutes

        return Response(response)
