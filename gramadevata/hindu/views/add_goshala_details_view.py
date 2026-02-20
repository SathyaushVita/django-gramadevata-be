from rest_framework import viewsets,status
from ..models import AddGoshalaDetails,Register
from ..serializers import AddGoshalaDetailsSerializer
from rest_framework .response import Response
from ..utils import save_image_to_azure,send_mail,save_video_to_azure,save_image_to_azure1
from django.utils import timezone
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import ast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from ..models import Goshala, AddGoshalaDetails



class AddGoshalaDetailsView(viewsets.ModelViewSet):
    queryset = AddGoshalaDetails.objects.all()
    serializer_class = AddGoshalaDetailsSerializer
    # permission_classes = []

    # def get_permissions(self):
    #     if self.request.method in ['GET', 'POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()



    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AddGoshalaDetailsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddGoshalaDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)
            register_instance = None

            if email:
                register_instance = Register.objects.filter(email=email).first()
            elif contact_number:
                register_instance = Register.objects.filter(contact_number=contact_number).first()

            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if register_instance.is_member == 'false':
                return Response({"message": "Cannot add more details. Membership details are required."})

            # Extract images and videos
            image_locations = request.data.get('image_location', [])
            video_files = request.data.get('goshala_video', [])  

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(video_files, list):
                video_files = [video_files]

            # Set placeholders to avoid errors
            request.data['image_location'] = "null"
            request.data['goshala_video'] = "null"

            # Serialize and save
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_videos = []
            saved_images = []

            # Process videos
            if video_files and "null" not in video_files:
                entity_type = "goshala"
                for goshala_video in video_files:
                    if goshala_video and goshala_video != "null":
                        saved_video = save_video_to_azure(goshala_video, serializer.instance._id, serializer.instance.goshala_id, entity_type)
                        if saved_video:
                            saved_videos.append(saved_video)

            # Process images
            if image_locations and "null" not in image_locations:
                entity_type = "goshala"
                for image in image_locations:
                    if image and image != "null":
                        saved_image = save_image_to_azure1(image, serializer.instance._id, serializer.instance.goshala_id, entity_type)
                        if saved_image:
                            saved_images.append(saved_image)

            # Update instance with saved paths
            if saved_videos:
                serializer.instance.goshala_video = saved_videos
                serializer.instance.save()
            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            # Send email notification
            created_at = timezone.now()
            send_mail(
                'Added More goshala Details',
                f'User ID: {request.user.id}\nCreated Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Added Details ID: {serializer.instance._id}\goshala ID: {serializer.instance.goshala_id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({"message": "success", "result": serializer.data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def retrieve(self, request, pk=None):
        try:
            instance = AddGoshalaDetails.objects.filter(_id=pk).first()

            if not instance:
                return Response(
                    {'message': 'Object not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = AddGoshalaDetailsSerializer(instance)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {'message': 'An error occurred', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


        
    def create(self, request, *args, **kwargs):
        try:
            # Membership check
            email = request.user.email
            contact_number = request.user.contact_number

            register_instance = Register.objects.filter(
                Q(email=email) | Q(contact_number=contact_number)
            ).first()

            if not register_instance or register_instance.is_member == 'false':
                return Response({"message": "Membership required"}, status=403)

            image_list = request.data.get('image_location', [])
            video_list = request.data.get('goshala_video', [])

            if not isinstance(image_list, list):
                image_list = [image_list]
            if not isinstance(video_list, list):
                video_list = [video_list]

            data = request.data.copy()
            data['image_location'] = []
            data['goshala_video'] = []

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            goshala_name = instance.desc or "goshala"

            # Upload images
            images = []
            for img in image_list:
                if img and img != "null":
                    path = save_image_to_azure1(img, instance._id, goshala_name, "goshala")
                    if path:
                        images.append(path)

            # Upload videos
            videos = []
            for vid in video_list:
                if vid and vid != "null":
                    path = save_video_to_azure(vid, instance._id, goshala_name, "goshala")
                    if path:
                        videos.append(path)

            # ✅ MERGE (IMPORTANT)
            instance.image_location = images
            instance.goshala_video = videos
            instance.save()

            send_mail(
                'Added goshala Details',
                f'Goshala ID: {instance.goshala_id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
            )

            return Response(
                {"message": "success", "result": AddGoshalaDetailsSerializer(instance).data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        instance = self.get_object()

        image_list = request.data.get('image_location', [])
        video_list = request.data.get('goshala_video', [])

        if not isinstance(image_list, list):
            image_list = [image_list]
        if not isinstance(video_list, list):
            video_list = [video_list]

        data = request.data.copy()
        data.pop('image_location', None)
        data.pop('goshala_video', None)

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        goshala_name = instance.desc or "Goshala"

        # Upload new images
        new_images = []
        for img in image_list:
            if img and img != "null":
                path = save_image_to_azure1(img, instance._id, goshala_name, "goshala")
                if path:
                    new_images.append(path)

        # Upload new videos
        new_videos = []
        for vid in video_list:
            if vid and vid != "null":
                path = save_video_to_azure(vid, instance._id, goshala_name, "goshala")
                if path:
                    new_videos.append(path)

        # ✅ APPEND (KEY FIX)
        instance.image_location = (instance.image_location or []) + new_images
        instance.goshala_video = (instance.goshala_video or []) + new_videos
        instance.save()

        return Response({
            "message": "updated successfully",
            "data": AddGoshalaDetailsSerializer(instance).data
        })




class AddMoreGoshalaDetailGoshalaMergeAPIView(APIView):

    def parse_list_field(self, raw):
        """Parses string or list into a Python list"""
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
    def put(self, request, goshala_id):
        try:
            # ✅ ALLOW ACTIVE + INACTIVE
            goshala = Goshala.objects.filter(_id=goshala_id).first()

            if not goshala:
                return Response(
                    {"message": "Goshala not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # -------- Incoming Data --------
            new_desc = request.data.get("desc", "")
            new_images = request.data.get("image_location", [])
            new_mapUrls = request.data.get("map_location", [])
            new_videos = request.data.get("goshala_video", [])

            # -------- Existing Goshala Data --------
            old_desc = goshala.desc or ""
            old_images = self.parse_images(goshala.image_location)
            old_mapUrls = self.parse_list_field(goshala.map_location)
            old_videos = self.parse_list_field(goshala.goshala_video)

            # -------- Previous AddGoshalaDetails --------
            details_qs = AddGoshalaDetails.objects.filter(goshala_id=goshala)

            all_descs, all_images, all_mapUrls, all_videos = [], [], [], []

            for d in details_qs:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += self.parse_images(d.image_location)
                all_mapUrls += self.parse_list_field(d.map_location)
                all_videos += self.parse_list_field(d.goshala_video)

            # -------- MERGE (NO DUPLICATES) --------
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

            # -------- SAVE TO GOSHALA (AUTO ACTIVATE) --------
            goshala.desc = merged_desc
            goshala.image_location = str(merged_images)   # stored as string
            goshala.map_location = str(merged_mapUrls)    # stored as string
            goshala.goshala_video = merged_videos

            goshala.status = "ACTIVE"   # ✅ AUTO ACTIVATE

            goshala.save()

            # -------- REPLACE ADDGOSHALADETAILS --------
            details_qs.delete()

            AddGoshalaDetails.objects.create(
                goshala_id=goshala,
                desc=merged_desc,
                image_location=str(merged_images),
                map_location=str(merged_mapUrls),
                goshala_video=merged_videos,
                status="ACTIVE"   # ✅ AUTO ACTIVE (if field exists)
            )

            # -------- RESPONSE --------
            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "goshala_id": str(goshala._id),
                "name": goshala.name,
                "desc": merged_desc,
                "image_location": [base_url + img for img in merged_images],
                "map_location": merged_mapUrls,
                "goshala_video": [base_url + v for v in merged_videos],
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": "Error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )