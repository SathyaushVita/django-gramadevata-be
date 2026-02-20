from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from ..models import AddWelfareHome, WelfareHomes, Register
from ..serializers import AddWelfareHomeSerializer
from ..utils import save_image_to_azure, send_mail
import json

class AddWelfareHomeViewSet(viewsets.ModelViewSet):
    queryset = AddWelfareHome.objects.all()
    serializer_class = AddWelfareHomeSerializer
    # permission_classes = [IsAuthenticated]

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

    # ---------------- CREATE ----------------
    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            register_instance = Register.objects.filter(
                Q(email=email) | Q(contact_number=contact_number)
            ).first()

            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if not getattr(register_instance, 'is_member', False):
                return Response({"message": "Membership required."}, status=status.HTTP_403_FORBIDDEN)

            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            data = request.data.copy()
            data['image_location'] = []

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=register_instance)

            saved_images = []
            name = serializer.instance.name

            for image in image_locations:
                if image and image != "null":
                    saved = save_image_to_azure(
                        image,
                        serializer.instance._id,
                        name,
                        "welfarehome"
                    )
                    if saved:
                        saved_images.append(saved)

            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            send_mail(
                'Added Welfare Home',
                f'User: {request.user.id}\nTime: {timezone.now()}\nID: {serializer.instance._id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
            )

            return Response({"message": "success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "Error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                        "welfarehome"
                    )
                    if saved:
                        saved_images.append(saved)

            if saved_images:
                # Merge old images with new ones (like TourismPlace)
                merged_images = list(dict.fromkeys(self.parse_images(instance.image_location) + saved_images))
                instance.image_location = merged_images
                instance.save()

            return Response({
                "message": "updated successfully",
                "data": self.get_serializer(instance).data
            })

        except Exception as e:
            return Response({"message": "Error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import json

from ..models import AddWelfareHome, WelfareHomes

class WelfareHomeMergeAPIView(APIView):

    def parse_images(self, raw):
        if isinstance(raw, list):
            return [img.strip().replace("\\", "/").lstrip("/") for img in raw if isinstance(img, str) and img.strip()]
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
        return [img.strip().strip('"').strip("'").replace("\\", "/").lstrip("/") for img in raw_list if img.strip()]

    def put(self, request, welfare_id):
        try:
            # ---------------- MASTER WELFARE HOME ----------------
            master = WelfareHomes.objects.filter(_id=welfare_id).first()
            if not master:
                return Response({"message": "Welfare Home not found."}, status=status.HTTP_404_NOT_FOUND)

            # ---------------- USER-ADDED ENTRIES ----------------
            entries = AddWelfareHome.objects.filter(welfare_id=master).order_by('created_at')

            # ---------------- NEW DATA ----------------
            new_desc = request.data.get("desc", "").strip()
            new_address = request.data.get("address", "").strip()
            new_website = request.data.get("website", "").strip()
            new_images = self.parse_images(request.data.get("image_location", []))

            activity_fields = [
                "medical_care", "food_and_shelter", "counseling_services", "rehabilitation_programs",
                "skill_training", "mental_health_support", "legal_aid", "is_24_7_support", "security",
                "education", "physiotherapy", "play_area", "recreational_activities", "adoption_services",
                "family_counseling", "emergency_response", "special_needs_support"
            ]
            new_activities = {field: request.data.get(field) for field in activity_fields if request.data.get(field) is not None}

            # ---------------- OLD DATA ----------------
            all_descs = [getattr(master, 'desc', '')] if getattr(master, 'desc', None) else []
            all_addresses = [getattr(master, 'address', '')] if getattr(master, 'address', None) else []
            all_websites = [getattr(master, 'website', '')] if getattr(master, 'website', None) else []
            all_images = self.parse_images(getattr(master, 'image_location', []))
            all_activities = {field: [getattr(master, field)] if getattr(master, field, None) else [] for field in activity_fields}

            # Add all user-added entries
            for e in entries:
                if e.desc: all_descs.append(e.desc.strip())
                if e.address: all_addresses.append(e.address.strip())
                if e.website: all_websites.append(e.website.strip())
                all_images += self.parse_images(e.image_location)
                for field in activity_fields:
                    val = getattr(e, field)
                    if val:
                        all_activities[field].append(val)

            # Add new request data
            if new_desc: all_descs.append(new_desc)
            if new_address: all_addresses.append(new_address)
            if new_website: all_websites.append(new_website)
            all_images += new_images
            for field, val in new_activities.items():
                if val: all_activities[field].append(val)

            # ---------------- MERGE ----------------
            merged_desc = ", ".join(dict.fromkeys(filter(None, all_descs)))
            merged_address = ", ".join(dict.fromkeys(filter(None, all_addresses)))
            merged_website = ", ".join(dict.fromkeys(filter(None, all_websites)))
            merged_images = list(dict.fromkeys(all_images))
            merged_activities = {field: ", ".join(dict.fromkeys(vals)) for field, vals in all_activities.items()}

            # ---------------- SAVE TO MASTER ----------------
            master.desc = merged_desc
            master.address = merged_address
            master.website = merged_website
            master.image_location = merged_images
            for field, val in merged_activities.items():
                setattr(master, field, val)
            master.status = "ACTIVE"
            master.save()

            # ---------------- RESPONSE ----------------
            base_url = settings.FILE_URL.rstrip("/") + "/"
            return Response({
                "welfare_home_id": str(master._id),
                "name": master.name,
                "desc": merged_desc,
                "address": merged_address,
                "website": merged_website,
                "image_location": [base_url + img for img in merged_images],
                **merged_activities,
                "status": master.status
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)