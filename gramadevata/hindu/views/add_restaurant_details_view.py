from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from ..models import AddRestaurantDetails, Register
from ..serializers import AddRestaurantDetailsSerializer
from ..utils import save_image_to_azure, save_video_to_azure, send_mail
import ast
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from ..models import AddRestaurantDetails

class AddRestaurantDetailsView(viewsets.ModelViewSet):
    queryset = AddRestaurantDetails.objects.all()
    serializer_class = AddRestaurantDetailsSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AddRestaurantDetailsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AddRestaurantDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = AddRestaurantDetailsSerializer(instance)
            return Response(serializer.data)
        except AddRestaurantDetails.DoesNotExist:
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
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            request.data['image_location'] = []

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            restaurant_name = serializer.instance.name
            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure(image, serializer.instance._id, restaurant_name, "restaurant")
                    if saved_image:
                        saved_images.append(saved_image)

            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            send_mail(
                'Added More Restaurant Details',
                f'User ID: {request.user.id}\nCreated Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Added Details ID: {serializer.instance._id}\nRestaurant Name: {serializer.instance.name}',
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
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            data = request.data.copy()
            data.pop('image_location', None)

            serializer = AddRestaurantDetailsSerializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            restaurant_name = instance.name
            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure(image, instance._id, restaurant_name, "restaurant")
                    if saved_image:
                        saved_images.append(saved_image)

            if saved_images:
                instance.image_location = saved_images
                instance.save()

            return Response({
                "message": "updated successfully",
                "data": AddRestaurantDetailsSerializer(instance).data
            })

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












class RestaurantMergeAPIView(APIView):

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
        return list(dict.fromkeys(results))

    # --------------------------------------------------
    # PUT API
    # --------------------------------------------------
    def put(self, request, restaurant_id):
        try:
            restaurant = AddRestaurantDetails.objects.filter(_id=restaurant_id).first()
            if not restaurant:
                return Response(
                    {"message": "Restaurant not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------------- NEW DATA ----------------
            new_desc = request.data.get("desc", "").strip()
            new_images = request.data.get("image_location", []) or []
            new_videos = request.data.get("event_video", []) or []
            new_map_location = self.clean_map_location(
                request.data.get("map_location", [])
            )

            # ---------------- OLD DATA ----------------
            old_desc = restaurant.desc or ""
            old_images = restaurant.image_location or []
            old_videos = restaurant.event_video or []
            old_map_location = self.clean_map_location(
                restaurant.map_location or []
            )

            # ---------------- DUPLICATE RECORDS ----------------
            duplicates = AddRestaurantDetails.objects.filter(
                name__iexact=restaurant.name
            ).exclude(_id=restaurant._id)

            all_descs, all_images, all_videos, all_map_locations = [], [], [], []

            for d in duplicates:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += d.image_location or []
                all_videos += d.event_video or []
                all_map_locations += self.clean_map_location(d.map_location)

            # ---------------- MERGE ----------------
            merged_desc = ", ".join(
                dict.fromkeys(
                    filter(None, [old_desc, *all_descs, new_desc])
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

            # ---------------- SAVE ----------------
            restaurant.desc = merged_desc
            restaurant.image_location = merged_images
            restaurant.event_video = merged_videos
            restaurant.map_location = merged_map_location
            restaurant.status = "ACTIVE"
            restaurant.save()

            # ---------------- CLEAN DUPLICATES ----------------
            duplicates.delete()

            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "restaurant_id": str(restaurant._id),
                "name": restaurant.name,
                "desc": merged_desc,
                "image_location": [base_url + i for i in merged_images],
                "event_video": [base_url + v for v in merged_videos],
                "map_location": merged_map_location,
                "status": "ACTIVE"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "Error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
