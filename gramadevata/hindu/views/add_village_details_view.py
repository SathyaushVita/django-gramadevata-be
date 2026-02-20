from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import AddVillageDetails, Village
from django.conf import settings
import json
import ast


from ..models import AddVillageDetails, Register
from ..serializers import AddVillageDetailsSerializer
from ..utils import save_image_to_azure, save_video_to_azure, send_mail,save_image_to_azure1



class AddVillageDetailsView(viewsets.ModelViewSet):
    queryset = AddVillageDetails.objects.all()
    serializer_class = AddVillageDetailsSerializer
    # permission_classes = [IsAuthenticated] 

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AddVillageDetailsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AddVillageDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = AddVillageDetailsSerializer(instance)
            return Response(serializer.data)

        except AddVillageDetails.DoesNotExist:
            return Response(
                {'message': 'Object not found'},
                status=status.HTTP_404_NOT_FOUND
            )


    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            register_instance = Register.objects.filter(
                Q(email=email) | Q(contact_number=contact_number)
            ).first()

            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if register_instance.is_member == 'false':
                return Response({"message": "Cannot add more details. Membership details are required."})

            image_locations = request.data.get('image_location', [])
            video_files = request.data.get('village_video', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(video_files, list):
                video_files = [video_files]

            request.data['image_location'] = []
            request.data['village_video'] = []

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images, saved_videos = [], []
            entity_type = "village"

            village_name = serializer.instance.village_id.name

            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure1(image, serializer.instance._id, village_name, entity_type)
                    if saved_image:
                        saved_images.append(saved_image)

            for village_video in video_files:
                if village_video and village_video != "null":
                    saved_video = save_video_to_azure(village_video, serializer.instance._id, village_name, entity_type)
                    if saved_video:
                        saved_videos.append(saved_video)

            if saved_images:
                serializer.instance.image_location = saved_images
            if saved_videos:
                serializer.instance.village_video = saved_videos
            if saved_images or saved_videos:
                serializer.instance.save()

            send_mail(
                'Added More Village Details',
                f'User ID: {request.user.id}\nCreated Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Added Details ID: {serializer.instance._id}\nVillage ID: {serializer.instance.village_id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({"message": "success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        instance = self.get_object()

        try:
            image_locations = request.data.get('image_location', [])
            video_files = request.data.get('village_video', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(video_files, list):
                video_files = [video_files]

            data = request.data.copy()
            data.pop('image_location', None)
            data.pop('village_video', None)

            serializer = AddVillageDetailsSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images, saved_videos = [], []
            entity_type = "village"
            village_name = instance.village_id.name

            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure1(image, instance._id, village_name, entity_type)
                    if saved_image:
                        saved_images.append(saved_image)

            for village_video in video_files:
                if village_video and village_video != "null":
                    saved_video = save_video_to_azure(village_video, instance._id, village_name, entity_type)
                    if saved_video:
                        saved_videos.append(saved_video)

            updated = False
            if saved_images:
                instance.image_location = saved_images
                updated = True
            if saved_videos:
                instance.village_video = saved_videos
                updated = True

            if updated:
                instance.save()

            return Response({
                "message": "updated successfully",
                "data": AddVillageDetailsSerializer(instance).data
            })

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class AddmorevillagedetailvillagemergeAPIView(APIView):

    # ---------- COMMON PARSER ----------
    def parse_list_field(self, raw):
        """
        Converts:
        - ['url']            -> ['url']
        - "['url']"          -> ['url']
        - "url"              -> ['url']
        - None / ""          -> []
        """
        if isinstance(raw, list):
            return [str(x).strip() for x in raw if str(x).strip()]

        if not raw:
            return []

        if isinstance(raw, str):
            try:
                parsed = ast.literal_eval(raw)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except:
                pass
            return [raw.strip()]

        return []

    # ---------- IMAGE PARSER ----------
    def parse_images(self, raw):
        return [
            img.replace("\\", "/").lstrip("/")
            for img in self.parse_list_field(raw)
        ]

    # ---------- PUT API ----------
    def put(self, request, village_id):
        try:
            # ✅ ALLOW ACTIVE + INACTIVE
            village = Village.objects.filter(_id=village_id).first()

            if not village:
                return Response(
                    {"message": "Village not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------- Incoming Data ----------
            new_desc = request.data.get("desc", "")
            new_images = request.data.get("image_location", [])
            new_mapUrls = request.data.get("mapUrl", [])
            new_videos = request.data.get("village_video", [])

            # ---------- Existing Village Data ----------
            old_desc = village.desc or ""
            old_images = self.parse_images(village.image_location)
            old_mapUrls = self.parse_list_field(village.mapUrl)
            old_videos = self.parse_list_field(village.village_video)

            # ---------- Previous AddVillageDetails ----------
            details_qs = AddVillageDetails.objects.filter(village_id=village)

            all_descs, all_images, all_mapUrls, all_videos = [], [], [], []

            for d in details_qs:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += self.parse_images(d.image_location)
                all_mapUrls += self.parse_list_field(d.mapUrl)
                all_videos += self.parse_list_field(d.village_video)

            # ---------- MERGE (NO DUPLICATES) ----------
            merged_desc = ", ".join(
                dict.fromkeys(
                    filter(None, [old_desc.strip(), *all_descs, new_desc.strip()])
                )
            )

            merged_images = list(dict.fromkeys(
                old_images + all_images + self.parse_images(new_images)
            ))

            merged_mapUrls = list(dict.fromkeys(
                old_mapUrls + all_mapUrls + self.parse_list_field(new_mapUrls)
            ))

            merged_videos = list(dict.fromkeys(
                old_videos + all_videos + self.parse_list_field(new_videos)
            ))

            # ---------- SAVE TO VILLAGE ----------
            village.desc = merged_desc
            village.image_location = merged_images
            village.mapUrl = merged_mapUrls
            village.village_video = merged_videos

            # ✅ AUTO ACTIVATE
            village.status = "ACTIVE"

            village.save()

            # ---------- REPLACE ADDVILLAGEDETAILS ----------
            details_qs.delete()

            AddVillageDetails.objects.create(
                village_id=village,
                desc=merged_desc,
                image_location=merged_images,
                mapUrl=merged_mapUrls,
                village_video=merged_videos,
                status="ACTIVE"   # ✅ AUTO ACTIVE
            )

            # ---------- RESPONSE ----------
            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "village_id": str(village._id),
                "name": village.name,
                "desc": merged_desc,
                "image_location": [base_url + img for img in merged_images],
                "mapUrl": merged_mapUrls,
                "village_video": [base_url + v for v in merged_videos],
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)