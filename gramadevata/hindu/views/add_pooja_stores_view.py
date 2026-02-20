from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
import ast
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from ..models import PoojaStore, AddMorePoojaStore
from ..models import AddMorePoojaStore, PoojaStore, Register
from ..serializers import AddMorePoojaStoreSerializer
from ..utils import save_image_to_azure, send_mail

class AddMorePoojaStoreViewSet(viewsets.ModelViewSet):
    queryset = AddMorePoojaStore.objects.all()
    serializer_class = AddMorePoojaStoreSerializer
    # permission_classes = [IsAuthenticated]  
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except AddMorePoojaStore.DoesNotExist:
            return Response({"message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)
            register_instance = Register.objects.filter(Q(email=email) | Q(contact_number=contact_number)).first()

            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            if register_instance.is_member == 'false':
                return Response({"message": "Cannot add more details. Membership details are required."})

            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            request.data['image_location'] = []

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            store_name = serializer.instance.pooja_store_id.name if serializer.instance.pooja_store_id else "pooja_store"
            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure(image, serializer.instance._id, store_name, "pooja_store")
                    if saved_image:
                        saved_images.append(saved_image)

            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            send_mail(
                'Added More Pooja Store Details',
                f'User ID: {request.user.id}\nCreated Time: {timezone.now()}\nPooja Store ID: {serializer.instance.pooja_store_id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({"message": "success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








class PoojaStoreMergeAPIView(APIView):

    # ---------------- SAFE MAP LOCATION PARSER ----------------
    def clean_map_location(self, raw):
        results = []

        def _clean(item):
            if not item:
                return

            if isinstance(item, list):
                for i in item:
                    _clean(i)
                return

            if isinstance(item, str):
                val = item.strip()

                # Handle stringified list
                if val.startswith("[") and val.endswith("]"):
                    try:
                        parsed = ast.literal_eval(val)
                        _clean(parsed)
                        return
                    except Exception:
                        pass

                val = val.replace("\\", "").strip("'\"")

                match = re.search(r"https://maps\.app\.goo\.gl/\S+", val)
                if match:
                    results.append(match.group())

        _clean(raw)
        return list(dict.fromkeys(results))  # remove duplicates

    # --------------------------------------------------
    # PUT API
    # --------------------------------------------------
    def put(self, request, pooja_store_id):
        try:
            store = PoojaStore.objects.filter(_id=pooja_store_id).first()
            if not store:
                return Response(
                    {"message": "Pooja Store not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------------- NEW DATA ----------------
            new_desc = request.data.get("desc", "").strip()
            new_images = request.data.get("image_location", []) or []
            new_map_location = self.clean_map_location(
                request.data.get("map_location", [])
            )

            # ---------------- OLD STORE DATA ----------------
            old_desc = store.desc or ""
            old_images = store.image_location or []
            old_map_location = self.clean_map_location(
                store.map_location or []
            )

            # ---------------- AddMorePoojaStore DATA ----------------
            details_qs = AddMorePoojaStore.objects.filter(
                pooja_store_id=store
            )

            all_descs, all_images, all_map_locations = [], [], []

            for d in details_qs:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += d.image_location or []
                all_map_locations += self.clean_map_location(d.map_location)

            # ---------------- MERGE (NO DUPLICATES) ----------------
            merged_desc = ", ".join(
                dict.fromkeys(
                    filter(None, [old_desc, *all_descs, new_desc])
                )
            )

            merged_images = list(dict.fromkeys(
                old_images + all_images + new_images
            ))

            merged_map_location = self.clean_map_location(
                old_map_location + all_map_locations + new_map_location
            )

            # ---------------- SAVE TO PoojaStore ----------------
            store.desc = merged_desc
            store.image_location = merged_images
            store.map_location = merged_map_location
            store.status = "ACTIVE"
            store.save()

            # ---------------- REPLACE AddMorePoojaStore ----------------
            details_qs.delete()

            AddMorePoojaStore.objects.create(
                pooja_store_id=store,
                desc=merged_desc,
                image_location=merged_images,
                map_location=merged_map_location,
                status="ACTIVE"
            )

            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "pooja_store_id": str(store._id),
                "name": store.name,
                "desc": merged_desc,
                "image_location": [base_url + img for img in merged_images],
                "map_location": merged_map_location,
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
