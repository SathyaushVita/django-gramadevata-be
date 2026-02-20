from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models import AddTourismPlace, Register
from ..serializers import AddTourismPlaceSerializer
from ..utils import save_image_to_azure, send_mail
import re
import ast


class AddTourismPlaceViewSet(viewsets.ModelViewSet):
    queryset = AddTourismPlace.objects.all()
    serializer_class = AddTourismPlaceSerializer
    # permission_classes = [IsAuthenticated]

    # ---------------- CREATE ----------------
    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            register_instance = Register.objects.filter(
                Q(email=email) | Q(contact_number=contact_number)
            ).first()

            if not register_instance:
                return Response(
                    {"message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ✅ FIXED BOOLEAN CHECK
            if not register_instance.is_member:
                return Response(
                    {"message": "Cannot add more details. Membership details are required."},
                    status=status.HTTP_403_FORBIDDEN
                )

            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            data = request.data.copy()
            data['image_location'] = []

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=register_instance)

            saved_images = []
            name = serializer.instance.name

            for image in image_locations:
                if image and image != "null":
                    saved = save_image_to_azure(
                        image,
                        serializer.instance._id,
                        name,
                        "tourismplace"
                    )
                    if saved:
                        saved_images.append(saved)

            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            send_mail(
                'Added Tourism Place',
                f'User: {request.user.id}\nTime: {timezone.now()}\nID: {serializer.instance._id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
            )

            return Response(
                {"message": "success", "result": serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ---------------- UPDATE ----------------
    def update(self, request, pk=None):
        instance = self.get_object()
        try:
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            data = request.data.copy()
            data.pop('image_location', None)

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            name = instance.name

            for image in image_locations:
                if image and image != "null":
                    saved = save_image_to_azure(
                        image,
                        instance._id,
                        name,
                        "tourismplace"
                    )
                    if saved:
                        saved_images.append(saved)

            if saved_images:
                instance.image_location = saved_images
                instance.save()

            return Response({
                "message": "updated successfully",
                "data": self.get_serializer(instance).data
            })

        except Exception as e:
            return Response(
                {"message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )








from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import ast
import re
import json

from ..models import AddTourismPlace, TempleNearbyTourismPlace


class TourismPlaceMergeAPIView(APIView):

    def parse_images(self, raw):
        if isinstance(raw, list):
            return [
                img.strip().replace("\\", "/").lstrip("/")
                for img in raw if isinstance(img, str) and img.strip()
            ]

        if not raw:
            return []

        s = str(raw).strip()
        try:
            lst = json.loads(s)
            if isinstance(lst, list):
                raw_list = lst
            elif isinstance(lst, str):
                raw_list = lst.split(",")
            else:
                raw_list = [str(lst)]
        except:
            raw_list = s.strip('[]"\'').split(",")

        return [
            img.strip().strip('"').strip("'").replace("\\", "/").lstrip("/")
            for img in raw_list if img.strip()
        ]

    def clean_map_location(self, raw):
        """Clean and merge map location URLs."""
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
                if val.startswith("[") and val.endswith("]"):
                    try:
                        parsed = ast.literal_eval(val)
                        _clean(parsed)
                        return
                    except:
                        pass
                val = val.replace("\\", "").strip("'\"")
                if "," in val:
                    results.extend([v.strip() for v in val.split(",") if v.strip()])
                else:
                    results.append(val)
        _clean(raw)
        return list(dict.fromkeys(results))  # remove duplicates

    def put(self, request, tourism_id):
        try:
            # ---------------- MASTER TOURISM ----------------
            tourism_master = TempleNearbyTourismPlace.objects.filter(_id=tourism_id).first()
            if not tourism_master:
                return Response({"message": "Tourism not found"}, status=status.HTTP_404_NOT_FOUND)

            # ---------------- USER-ADDED DETAILS ----------------
            entries = AddTourismPlace.objects.filter(tourism_id=tourism_master).order_by('created_at')

            # ---------------- NEW DATA ----------------
            new_desc = request.data.get("desc", "").strip()
            new_type = request.data.get("type", "").strip()
            new_timings = request.data.get("timings", "").strip()
            new_address = request.data.get("address", "").strip()
            new_images = self.parse_images(request.data.get("image_location", []))
            new_map_location = self.clean_map_location(request.data.get("map_location", []))

            # ---------------- OLD DATA ----------------
            all_descs = [tourism_master.desc] if tourism_master.desc else []
            all_types = [tourism_master.type] if tourism_master.type else []
            all_timings = [tourism_master.timings] if tourism_master.timings else []
            all_addresses = [tourism_master.address] if tourism_master.address else []
            all_images = self.parse_images(tourism_master.image_location)
            all_map_locations = self.clean_map_location(tourism_master.map_location)

            # Add all user-added entries
            for e in entries:
                if e.desc: all_descs.append(e.desc.strip())
                if e.type: all_types.append(e.type.strip())
                if e.timings: all_timings.append(e.timings.strip())
                if e.address: all_addresses.append(e.address.strip())
                all_images += self.parse_images(e.image_location)
                all_map_locations += self.clean_map_location(e.map_location)

            # Add new request data
            if new_desc: all_descs.append(new_desc)
            if new_type: all_types.append(new_type)
            if new_timings: all_timings.append(new_timings)
            if new_address: all_addresses.append(new_address)
            all_images += new_images
            all_map_locations += new_map_location

            # ---------------- MERGE ----------------
            merged_desc = ", ".join(dict.fromkeys(filter(None, all_descs)))
            merged_type = ", ".join(dict.fromkeys(filter(None, all_types)))
            merged_timings = ", ".join(dict.fromkeys(filter(None, all_timings)))
            merged_address = ", ".join(dict.fromkeys(filter(None, all_addresses)))
            merged_images = list(dict.fromkeys(all_images))
            merged_map_location = list(dict.fromkeys(all_map_locations))

            # ---------------- SAVE TO MASTER ----------------
            tourism_master.desc = merged_desc
            tourism_master.type = merged_type
            tourism_master.timings = merged_timings
            tourism_master.address = merged_address
            tourism_master.image_location = merged_images
            tourism_master.map_location = merged_map_location
            tourism_master.status = "ACTIVE"
            tourism_master.save()

            # ---------------- RESPONSE ----------------
            base_url = settings.FILE_URL.rstrip("/") + "/"
            return Response({
                "tourism_id": str(tourism_master._id),
                "name": tourism_master.name,
                "desc": merged_desc,
                "type": merged_type,
                "timings": merged_timings,
                "address": merged_address,
                "image_location": [base_url + img for img in merged_images],
                "map_location": merged_map_location,
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)