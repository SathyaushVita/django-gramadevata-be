from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mail, EmailMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from ..serializers import VeterinaryHospitalSerializer,VeterinaryHospitalSerializer1,InactiveVeterinaryHospitalSerializer
from ..models import VeterinaryHospital
from ..serializers import VeterinaryHospitalSerializer
from ..utils import save_image_to_azure  

class NearbyVeterinaryHospitalViewSet(viewsets.ModelViewSet):
    queryset = VeterinaryHospital.objects.all()
    serializer_class = VeterinaryHospitalSerializer

    def get_queryset(self):
        filter_kwargs = {'status': 'ACTIVE'}
        for key, value in self.request.query_params.items():
            filter_kwargs[key] = value
        return VeterinaryHospital.objects.filter(**filter_kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'ACTIVE':
            return Response({'message': 'Data not found', 'status': 404}, status=404)
        return super().retrieve(request, *args, **kwargs)



    def create(self, request, *args, **kwargs):
        try:
            # ---------------- FILE INPUT ----------------
            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # ---------------- TEMP SAVE ----------------
            request.data['image_location'] = "null"
            request.data['license_copy'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = []
            saved_license_copies = []

            # ---------------- IMAGE UPLOAD ----------------
            if image_locations and "null" not in image_locations:
                for image in image_locations:
                    if image and image != "null":
                        path = save_image_to_azure(
                            image,
                            serializer.instance._id,
                            serializer.instance.name,
                            "veterinary_hospital"
                        )
                        if path:
                            saved_image_locations.append(path)

            # ---------------- LICENSE UPLOAD ----------------
            if license_copies and "null" not in license_copies:
                for file in license_copies:
                    if file and file != "null":
                        path = save_image_to_azure(
                            file,
                            serializer.instance._id,
                            serializer.instance.name,
                            "veterinary_license"
                        )
                        if path:
                            saved_license_copies.append(path)

            # ---------------- SAVE PATHS ----------------
            if saved_image_locations:
                serializer.instance.image_location = saved_image_locations

            if saved_license_copies:
                serializer.instance.license_copy = saved_license_copies

            serializer.instance.save()

            # ---------------- USER DETAILS ----------------
            created_at = timezone.now()

            if request.user and request.user.is_authenticated:
                user_name = request.user.get_full_name() or request.user.username
                user_email = request.user.email
            else:
                user_name = "Anonymous"
                user_email = None

            # ---------------- ADMIN MAIL (WITH REPLY-TO USER) ----------------
            admin_email = EmailMessage(
                subject="New Veterinary Hospital Added",
                body=(
                    f"Hospital ID: {serializer.instance._id}\n"
                    f"Hospital Name: {serializer.instance.name}\n"
                    f"Created Time: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"Added By: {user_name}\n"
                    f"User Email: {user_email or 'N/A'}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[user_email] if user_email else None
            )
            admin_email.send(fail_silently=False)

            # ---------------- USER MAIL ----------------
            if user_email:
                send_mail(
                    subject="Veterinary Hospital Added Successfully",
                    message=(
                        f"Hi {user_name},\n\n"
                        f"Your veterinary hospital \"{serializer.instance.name}\" "
                        f"has been added successfully.\n\n"
                        f"Hospital ID: {serializer.instance._id}\n\n"
                        f"Thanks & Regards,\n"
                        f"Sathayush Tech Solutions"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email],
                    fail_silently=False,
                )

            return Response(
                {
                    "message": "success",
                    "result": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "message": "An error occurred",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if instance.status != 'ACTIVE':
                return Response(
                    {'message': 'Data not found', 'status': 404},
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------------- FILE INPUT ----------------
            image_locations = request.data.get('image_location', [])
            license_copies = request.data.get('license_copy', [])

            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            if not isinstance(license_copies, list):
                license_copies = [license_copies]

            # ---------------- TEMP VALUES FOR SERIALIZER ----------------
            request.data['image_location'] = instance.image_location or "null"
            request.data['license_copy'] = instance.license_copy or "null"

            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=True   # supports PATCH
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_image_locations = instance.image_location or []
            saved_license_copies = instance.license_copy or []

            # ---------------- IMAGE UPLOAD ----------------
            if image_locations and "null" not in image_locations:
                for image in image_locations:
                    if image and image != "null":
                        path = save_image_to_azure(
                            image,
                            instance._id,
                            instance.name,
                            "veterinary_hospital"
                        )
                        if path:
                            saved_image_locations.append(path)

            # ---------------- LICENSE UPLOAD ----------------
            if license_copies and "null" not in license_copies:
                for file in license_copies:
                    if file and file != "null":
                        path = save_image_to_azure(
                            file,
                            instance._id,
                            instance.name,
                            "veterinary_license"
                        )
                        if path:
                            saved_license_copies.append(path)

            # ---------------- SAVE PATHS ----------------
            if saved_image_locations:
                instance.image_location = saved_image_locations

            if saved_license_copies:
                instance.license_copy = saved_license_copies

            instance.save()

            return Response(
                {
                    "message": "Veterinary Hospital updated successfully",
                    "result": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except VeterinaryHospital.DoesNotExist:
            return Response(
                {"message": "Veterinary Hospital not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": "An error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
















class GetVeterinaryHospitalsByLocation(APIView):

    def get_queryset_filter(self, input_value, search_query=None):
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = (
            country_query |
            state_query |
            district_query |
            block_query |
            village_query
        )

        queryset = (
            VeterinaryHospital.objects
            .filter(combined_query, status='ACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
                'temple_id',
                'goshala_id'
            )
        )

        # 🔍 Search by hospital / doctor / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(doctor_name__icontains=search_query)
            )

        # 🔁 Fallback: direct village id
        if not queryset.exists():
            queryset = VeterinaryHospital.objects.filter(
                village_id=input_value,
                status='ACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(doctor_name__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        hospitals = self.get_queryset_filter(input_value, search_query)

        return Response({
            "veterinary_hospitals": VeterinaryHospitalSerializer1(hospitals, many=True).data
        })










class InactiveVeterinaryHospitalAPIView(APIView):
    """
    API to get only INACTIVE Veterinary Hospitals
    """

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Dynamic filtering (except search)
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Filter only INACTIVE records
        queryset = VeterinaryHospital.objects.filter(
            status='INACTIVE',
            **filter_kwargs
        )

        # Search by name or address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) 
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response(
                {"message": "Data not found", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InactiveVeterinaryHospitalSerializer(queryset, many=True)

        return Response({
            "count": queryset.count(),
            "inactive_veterinary_hospitals": serializer.data
        }, status=status.HTTP_200_OK)










class GetInactiveVeterinaryHospitalsByLocation(APIView):

    def get_queryset_filter(self, input_value, search_query=None):
        country_query = Q(village_id__block__district__state__country__pk=input_value)
        state_query = Q(village_id__block__district__state__pk=input_value)
        district_query = Q(village_id__block__district__pk=input_value)
        block_query = Q(village_id__block__pk=input_value)
        village_query = Q(village_id__pk=input_value)

        combined_query = (
            country_query |
            state_query |
            district_query |
            block_query |
            village_query
        )

        queryset = (
            VeterinaryHospital.objects
            .filter(combined_query, status='INACTIVE')
            .select_related(
                'village_id',
                'village_id__block',
                'village_id__block__district',
                'village_id__block__district__state',
                'village_id__block__district__state__country',
                'temple_id',
                'goshala_id'
            )
        )

        # 🔍 Search by hospital / doctor / address
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(doctor_name__icontains=search_query)
            )

        # 🔁 Fallback: direct village id
        if not queryset.exists():
            queryset = VeterinaryHospital.objects.filter(
                village_id=input_value,
                status='INACTIVE'
            )
            if search_query:
                queryset = queryset.filter(
                    Q(name__icontains=search_query) |
                    Q(address__icontains=search_query) |
                    Q(doctor_name__icontains=search_query)
                )

        return queryset

    def get(self, request):
        input_value = request.query_params.get('input_value')
        if not input_value:
            raise ValidationError("input_value is required")

        search_query = request.query_params.get('search', '').strip()

        hospitals = self.get_queryset_filter(input_value, search_query)

        return Response({
            "veterinary_hospitals": InactiveVeterinaryHospitalSerializer(hospitals, many=True).data
        })



