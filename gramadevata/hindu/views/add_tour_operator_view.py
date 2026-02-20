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

from ..models import AddTourOperator
from ..models import AddTourOperator, Register
from ..serializers import AddTourOperatorSerializer
from ..utils import save_image_to_azure, send_mail

class AddTourOperatorViewSet(viewsets.ModelViewSet):
    queryset = AddTourOperator.objects.all()
    serializer_class = AddTourOperatorSerializer
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
        except AddTourOperator.DoesNotExist:
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
            operator_name = serializer.instance.tour_operator_name
            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure(image, serializer.instance._id, operator_name, "tour_operator")
                    if saved_image:
                        saved_images.append(saved_image)

            if saved_images:
                serializer.instance.image_location = saved_images
                serializer.instance.save()

            send_mail(
                'Added Tour Operator',
                f'User ID: {request.user.id}\nCreated Time: {timezone.now()}\nOperator ID: {serializer.instance._id}',
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

            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            operator_name = instance.tour_operator_name
            for image in image_locations:
                if image and image != "null":
                    saved_image = save_image_to_azure(image, instance._id, operator_name, "tour_operator")
                    if saved_image:
                        saved_images.append(saved_image)

            if saved_images:
                instance.image_location = saved_images
                instance.save()

            return Response({
                "message": "updated successfully",
                "data": self.get_serializer(instance).data
            })

        except Exception as e:
            return Response({"message": "An error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










class TourOperatorMergeAPIView(APIView):

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
    def put(self, request, operator_id):
        try:
            operator = AddTourOperator.objects.filter(_id=operator_id).first()
            if not operator:
                return Response(
                    {"message": "Tour Operator not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------------- NEW DATA ----------------
            new_desc = request.data.get("desc", "").strip()
            new_images = request.data.get("image_location", []) or []
            new_map_location = self.clean_map_location(
                request.data.get("map_location", [])
            )

            # ---------------- OLD DATA ----------------
            old_desc = operator.desc or ""
            old_images = operator.image_location or []
            old_map_location = self.clean_map_location(
                operator.map_location or []
            )

            # ---------------- DUPLICATE OPERATORS ----------------
            duplicates = AddTourOperator.objects.filter(
                tour_operator_name__iexact=operator.tour_operator_name
            ).exclude(_id=operator._id)

            all_descs, all_images, all_map_locations = [], [], []

            for d in duplicates:
                if d.desc:
                    all_descs.append(d.desc.strip())
                all_images += d.image_location or []
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

            merged_map_location = self.clean_map_location(
                old_map_location + all_map_locations + new_map_location
            )

            # ---------------- SAVE ----------------
            operator.desc = merged_desc
            operator.image_location = merged_images
            operator.map_location = merged_map_location
            operator.status = "ACTIVE"
            operator.save()

            # ---------------- CLEAN DUPLICATES ----------------
            duplicates.delete()

            base_url = settings.FILE_URL.rstrip("/") + "/"

            return Response({
                "operator_id": str(operator._id),
                "tour_operator_name": operator.tour_operator_name,
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













