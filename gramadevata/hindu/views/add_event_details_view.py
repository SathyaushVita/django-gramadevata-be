from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from ..models import AddEventDetails, Register
from ..serializers import AddEventDetailsSerializer
from ..utils import save_image_to_azure, save_video_to_azure, send_mail,save_image_to_azure1
import ast, os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from ..models import Event, AddEventDetails
import re



class AddEventDetailsView(viewsets.ModelViewSet):
    queryset = AddEventDetails.objects.all()
    serializer_class = AddEventDetailsSerializer
    # permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AddEventDetailsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AddEventDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object() 
            serializer = AddEventDetailsSerializer(instance)
            return Response(serializer.data)

        except AddEventDetails.DoesNotExist:
            return Response(
                {'message': 'Object not found'},
                status=status.HTTP_404_NOT_FOUND
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
            video_list = request.data.get('event_video', [])
            if not isinstance(image_list, list):
                image_list = [image_list]
            if not isinstance(video_list, list):
                video_list = [video_list]
            data = request.data.copy()
            data['image_location'] = []
            data['event_video'] = []
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            event_name = instance.desc or "Event"
            # Upload images
            images = []
            for img in image_list:
                if img and img != "null":
                    path = save_image_to_azure1(img, instance._id, event_name, "events")
                    if path:
                        images.append(path)
            # Upload videos
            videos = []
            for vid in video_list:
                if vid and vid != "null":
                    path = save_video_to_azure(vid, instance._id, event_name, "events")
                    if path:
                        videos.append(path)
            # :white_check_mark: MERGE (IMPORTANT)
            instance.image_location = images
            instance.event_video = videos
            instance.save()
            send_mail(
                'Added Event Details',
                f'Event ID: {instance.event_id}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
            )
            return Response(
                {"message": "success", "result": AddEventDetailsSerializer(instance).data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def update(self, request, pk=None):
        instance = self.get_object()
        image_list = request.data.get('image_location', [])
        video_list = request.data.get('event_video', [])
        if not isinstance(image_list, list):
            image_list = [image_list]
        if not isinstance(video_list, list):
            video_list = [video_list]
        data = request.data.copy()
        data.pop('image_location', None)
        data.pop('event_video', None)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        event_name = instance.desc or "Event"
        # Upload new images
        new_images = []
        for img in image_list:
            if img and img != "null":
                path = save_image_to_azure1(img, instance._id, event_name, "event")
                if path:
                    new_images.append(path)
        # Upload new videos
        new_videos = []
        for vid in video_list:
            if vid and vid != "null":
                path = save_video_to_azure(vid, instance._id, event_name, "event")
                if path:
                    new_videos.append(path)
        # :white_check_mark: APPEND (KEY FIX)
        instance.image_location = (instance.image_location or []) + new_images
        instance.event_video = (instance.event_video or []) + new_videos
        instance.save()
        return Response({
            "message": "updated successfully",
            "data": AddEventDetailsSerializer(instance).data
        })






class AddMoreEventDetailEventMergeAPIView(APIView):

    # ---------- SAFE LIST PARSER ----------
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
    def put(self, request, event_id):
        try:
            # ✅ ALLOW ACTIVE + INACTIVE
            event = Event.objects.filter(_id=event_id).first()

            if not event:
                return Response(
                    {"message": "Event not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # -----------------------------
            # NEW DATA
            # -----------------------------
            new_desc = request.data.get("desc", "").strip()
            new_images = request.data.get("image_location", []) or []
            new_videos = request.data.get("event_video", []) or []
            new_map_location = self.clean_map_location(
                request.data.get("map_location", [])
            )

            # -----------------------------
            # OLD EVENT DATA
            # -----------------------------
            old_desc = event.desc or ""
            old_images = event.image_location or []
            old_videos = event.event_video or []
            old_map_location = self.clean_map_location(
                event.map_location or []
            )

            # -----------------------------
            # PREVIOUS AddEventDetails DATA
            # -----------------------------
            details_qs = AddEventDetails.objects.filter(event_id=event)

            all_descs, all_images, all_videos, all_map_locations = [], [], [], []

            for d in details_qs:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += d.image_location or []
                all_videos += d.event_video or []
                all_map_locations += self.clean_map_location(d.map_location)

            # -----------------------------
            # MERGE (NO DUPLICATES)
            # -----------------------------
            merged_desc = ", ".join(
                dict.fromkeys(
                    filter(None, [old_desc.strip(), *all_descs, new_desc])
                )
            )

            merged_images = list(dict.fromkeys(
                old_images + all_images + new_images
            ))

            merged_videos = list(dict.fromkeys(
                old_videos + all_videos + new_videos
            ))

            merged_map_location = self.clean_map_location(
                old_map_location + all_map_locations + new_map_location
            )

            # -----------------------------
            # SAVE TO EVENT (AUTO ACTIVATE)
            # -----------------------------
            event.desc = merged_desc
            event.image_location = merged_images
            event.event_video = merged_videos
            event.map_location = merged_map_location

            event.status = "ACTIVE"   # ✅ AUTO ACTIVATE

            event.save()

            # -----------------------------
            # REPLACE AddEventDetails
            # -----------------------------
            details_qs.delete()

            AddEventDetails.objects.create(
                event_id=event,
                desc=merged_desc,
                image_location=merged_images,
                event_video=merged_videos,
                map_location=merged_map_location,
                status="ACTIVE"   # ✅ if field exists
            )

            # -----------------------------
            # RESPONSE
            # -----------------------------
            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "event_id": str(event._id),
                "name": event.name,
                "desc": merged_desc,
                "image_location": [base_url + img for img in merged_images],
                "event_video": [base_url + v for v in merged_videos],
                "map_location": merged_map_location,
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
