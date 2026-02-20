from rest_framework import viewsets,status
from ..models import AddTempleDetails,Register
from ..serializers import AddTempleDetailsSerializer
from rest_framework .response import Response
from ..utils import save_image_to_azure,send_mail,save_video_to_azure,save_image_to_azure1
from django.utils import timezone
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework import status
from ..models import AddTempleDetails,Temple
from ..utils import save_image_to_azure
import json

from ..models import AddTempleDetails, Register
from django.core.mail import send_mail

class AddTempleDetailsView(viewsets.ModelViewSet):
    queryset = AddTempleDetails.objects.all()
    serializer_class = AddTempleDetailsSerializer
    permission_classes = []

    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        queryset = self.get_queryset()

        # Additional filtering based on query parameters
        temple_id = request.query_params.get('temple_id')
        user_id = request.query_params.get('user_id')

        if temple_id:
            queryset = queryset.filter(temple_id=temple_id)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        # Handle pagination and response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AddTempleDetailsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AddTempleDetailsSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()  
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"message": "An error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

            image_locations = request.data.get('image_location', [])
            videos = request.data.get('video', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            if not isinstance(videos, list):
                videos = [videos]

            request.data['image_location'] = "null"
            request.data['video'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            saved_videos = []
            entity_type = "temple"

            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure1(image, serializer.instance._id, serializer.instance.temple_id, entity_type)
                    if saved_image:
                        saved_images.append(saved_image)

            for video in videos:
                if video and video != "null":
                    saved_video = save_video_to_azure(video, serializer.instance._id, serializer.instance.temple_id, entity_type)
                    if saved_video:
                        saved_videos.append(saved_video)

            updated = False
            if saved_images:
                serializer.instance.image_location = saved_images
                updated = True
            if saved_videos:
                serializer.instance.video = saved_videos
                updated = True

            if updated:
                serializer.instance.save()

            created_at = timezone.now()
            send_mail(
                'Added More Temple Details',
                f'User ID: {request.user.id}\nCreated Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Added Details ID: {serializer.instance._id}\nTemple ID: {serializer.instance.temple_id}',
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
            image_locations = request.data.get('image_location')
            videos = request.data.get('video')

            data = request.data.copy()
            data.pop('image_location', None)
            data.pop('video', None)

            serializer = AddTempleDetailsSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            updated = False
            saved_images = []
            saved_videos = []

            entity_type = "temple"

            if image_locations is not None:
                if not isinstance(image_locations, list):
                    image_locations = [image_locations]
                for image in image_locations:
                    if image and image != "null":
                        saved_image = save_image_to_azure1(image, instance._id, instance.temple_id, entity_type)
                        if saved_image:
                            saved_images.append(saved_image)
                if saved_images:
                    instance.image_location = saved_images
                    updated = True

            if videos is not None:
                if not isinstance(videos, list):
                    videos = [videos]
                for video in videos:
                    if video and video != "null":
                        saved_video = save_video_to_azure(video, instance._id, instance.temple_id, entity_type)
                        if saved_video:
                            saved_videos.append(saved_video)
                if saved_videos:
                    instance.video = saved_videos
                    updated = True

            if updated:
                instance.save()

            return Response({
                "message": "Updated successfully",
                "data": AddTempleDetailsSerializer(instance).data
            })

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class AddmoretempledetailtemplemergeAPIView(APIView):

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

    def put(self, request, temple_id):
        try:
            new_desc = request.data.get("desc", "")
            new_images = request.data.get("image_location", [])

            # ✅ ALLOW ACTIVE + INACTIVE
            temple = Temple.objects.filter(_id=temple_id).first()

            if not temple:
                return Response(
                    {'message': 'Temple not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # -------- OLD DATA --------
            old_desc = temple.desc or ""
            old_imgs = self.parse_images(temple.image_location)

            # -------- NEW DATA --------
            parsed_new_imgs = self.parse_images(new_images)

            # -------- PREVIOUS DETAILS --------
            all_details = AddTempleDetails.objects.filter(temple_id=temple)

            all_descs = [d.desc.strip() for d in all_details if d.desc]
            all_imgs = []

            for d in all_details:
                all_imgs += self.parse_images(d.image_location)

            # -------- MERGE --------
            merged_desc = ", ".join(
                dict.fromkeys(
                    filter(None, [old_desc.strip(), *all_descs, new_desc.strip()])
                )
            )

            merged_paths = list(dict.fromkeys(
                old_imgs + all_imgs + parsed_new_imgs
            ))

            full_urls = [
                settings.FILE_URL.rstrip("/") + "/" + p
                for p in merged_paths
            ]

            # -------- SAVE TO TEMPLE (AUTO ACTIVE) --------
            temple.desc = merged_desc
            temple.image_location = merged_paths
            temple.status = "ACTIVE"    # ✅ AUTO ACTIVATE
            temple.save()

            # -------- REPLACE DETAILS --------
            all_details.delete()

            AddTempleDetails.objects.create(
                temple_id=temple,
                desc=merged_desc,
                image_location=merged_paths,
                status="ACTIVE"    # ✅ if field exists
            )

            return Response({
                "temple_id": str(temple._id),
                "name": temple.name,
                "desc": merged_desc,
                "image_location": full_urls,
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Error occurred',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)