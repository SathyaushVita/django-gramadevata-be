from rest_framework import viewsets, generics,status
from ..models import *
from ..serializers import *
from rest_framework .response import Response
from rest_framework .views import APIView
from django.db.models import Q
from rest_framework import viewsets, pagination
from ..serializers.temple_serializers import save_image_to_folder
from ..utils import save_image_to_folder,save_image_to_azure,save_video_to_azure
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters
from ..filters import TempleFilter
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import models 
from django.db.models.functions import Lower


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Case, When, IntegerField

from django.core.mail import EmailMultiAlternatives

class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000  



class TempleView(viewsets.ModelViewSet):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer
    pagination_class = CustomPagination




    filter_backends = [DjangoFilterBackend, SearchFilter]  # Required for search
    search_fields = ['name', 'address']  # Adjust fields as needed



    def list(self, request):
        queryset = self.get_queryset().filter(status='ACTIVE')
    # Priority IDs
        Main = "d7df749f-97e8-4635-a211-371c44b3c31f"
        Famous = "630f3239-f515-47fb-be8d-db727b9f2174"
        Highest = "b782cfa1-d0b5-11ee-84bd-0242ac110002"
        Lowest = "b78ac071-d0b5-11ee-84bd-0242ac110002"
    # Annotate and Order by Priority IDs
        queryset = queryset.annotate(
        order_priority=Case(
        When(priority__name="Iconic Temples  (Daily 2000 And Above Visitors)", then=0),
        When(priority__name="Famous (Daily 500 And Above Visitors)", then=1),
        When(priority__name="Area Temples  (Daily 100 And Above Visitors)", then=2),
        When(priority__name="Village Temples", then=3),
        # When(priority__name="Lowest", then=4),
        default=4,
        output_field=IntegerField()
    )
    )
        queryset = queryset.annotate(
        order_category=Case(
        When(category_id="742ecf7b-d0b5-11ee-84bd-0242ac110002", then=0),
        When(category_id="742c4b08-d0b5-11ee-84bd-0242ac110002", then=1),
        When(category_id="742c309e-d0b5-11ee-84bd-0242ac110002", then=2),
        When(category_id="742c043d-d0b5-11ee-84bd-0242ac110002", then=3),
        When(category_id="405033fe-fb78-49e0-aef9-35172863466c", then=4),
        When(category_id="11633522-2084-4f76-b360-0a0038c3f285", then=5),
        When(category_id="743339d5-d0b5-11ee-84bd-0242ac110002", then=6),
        When(category_id="74333d89-d0b5-11ee-84bd-0242ac110002", then=7),
        When(category_id="74333f6a-d0b5-11ee-84bd-0242ac110002", then=8),
        When(category_id="72524742-6e3a-4c2a-b4d4-4a0a68b5faa7", then=9),
        When(category_id="742f645c-d0b5-11ee-84bd-0242ac110002", then=10),
        When(category_id="74343760-d0b5-11ee-84bd-0242ac110002", then=11),
        When(category_id="742f66d4-d0b5-11ee-84bd-0242ac110002", then=12),
        When(category_id="742ed15f-d0b5-11ee-84bd-0242ac110002", then=13),
        When(category_id="74353e76-d0b5-11ee-84bd-0242ac110002", then=14),
        When(category_id="74334755-d0b5-11ee-84bd-0242ac110002", then=15),
        When(category_id="742fb823-d0b5-11ee-84bd-0242ac110002", then=16),
        When(category_id="7434333a-d0b5-11ee-84bd-0242ac110002", then=17),
        When(category_id="7433a0e7-d0b5-11ee-84bd-0242ac110002", then=18),
        When(category_id="74344055-d0b5-11ee-84bd-0242ac110002", then=19),
        When(category_id="742ecbf6-d0b5-11ee-84bd-0242ac110002", then=20),
        When(category_id="742e85ad-d0b5-11ee-84bd-0242ac110002", then=21),
        When(category_id="74345ef3-d0b5-11ee-84bd-0242ac110002", then=22),
        When(category_id="74353c0d-d0b5-11ee-84bd-0242ac110002", then=23),
        When(category_id="742ed999-d0b5-11ee-84bd-0242ac110002", then=24),
        When(category_id="742b10a6-d0b5-11ee-84bd-0242ac110002", then=25),
        When(category_id="742da6dc-d0b5-11ee-84bd-0242ac110002", then=26),
        When(category_id="742f57d9-d0b5-11ee-84bd-0242ac110002", then=27),
        When(category_id="74344b60-d0b5-11ee-84bd-0242ac110002", then=28),
        When(category_id="742c8632-d0b5-11ee-84bd-0242ac110002", then=29),
        When(category_id="742ee33e-d0b5-11ee-84bd-0242ac110002", then=30),
        When(category_id="742ccfe6-d0b5-11ee-84bd-0242ac110002", then=31),
        When(category_id="742cc4f8-d0b5-11ee-84bd-0242ac110002", then=32),
        When(category_id="742c5302-d0b5-11ee-84bd-0242ac110002", then=33),
        When(category_id="742da3d3-d0b5-11ee-84bd-0242ac110002", then=34),
        When(category_id="742f52be-d0b5-11ee-84bd-0242ac110002", then=35),
        When(category_id="74339dc3-d0b5-11ee-84bd-0242ac110002", then=36),
        When(category_id="743525d3-d0b5-11ee-84bd-0242ac110002", then=37),
        When(category_id="742f2965-d0b5-11ee-84bd-0242ac110002", then=38),
        When(category_id="742c0c1b-d0b5-11ee-84bd-0242ac110002", then=39),
        When(category_id="742c1781-d0b5-11ee-84bd-0242ac110002", then=40),
        When(category_id="742ebd7b-d0b5-11ee-84bd-0242ac110002", then=41),
        When(category_id="fee05763-b9b1-49d5-8423-b385625045ff", then=42),
        When(category_id="743340c9-d0b5-11ee-84bd-0242ac110002", then=43),
        When(category_id="a19958cc-86c2-44fc-a8f2-35c54208fae5", then=44),
        When(category_id="742fc433-d0b5-11ee-84bd-0242ac110002", then=45),
        When(category_id="142a703b-e8ad-4550-b68a-6a0718b90922", then=46),
        When(category_id="49eabde2-ce67-426a-a0ad-e51849910401", then=47),
        When(category_id="d4f979f4-2f7a-4aab-9782-702b31a21087", then=48),
        When(category_id="742fc5ca-d0b5-11ee-84bd-0242ac110002", then=49),
        When(category_id="6af7ab24-9a0e-42cb-a57a-372bc62cd842", then=50),
        default=51,
        output_field=IntegerField()
        )).order_by('order_category','order_priority')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TempleDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TempleDetailSerializer(queryset, many=True)
        return Response(serializer.data)



    # def create(self, request, *args, **kwargs):
    #     try:
    #         # Handle image upload
    #         image_locations = request.data.get('image_location', [])
    #         if not isinstance(image_locations, list):
    #             image_locations = [image_locations]
    #         request.data['image_location'] = "null"

    #         # Handle video upload
    #         temple_videos = request.data.get('temple_video', [])
    #         if not isinstance(temple_videos, list):
    #             temple_videos = [temple_videos]
    #         request.data['temple_video'] = "null"

    #         # Save main temple data
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         saved_images = []
    #         saved_videos = []

    #         entity_type = "temple"

    #         # Save images to Azure
    #         if image_locations and "null" not in image_locations:
    #             for image in image_locations:
    #                 if image and image != "null":
    #                     saved_location = save_image_to_azure(image, serializer.instance._id, serializer.instance.name, entity_type)
    #                     if saved_location:
    #                         saved_images.append(saved_location)

    #         # Save videos to Azure
    #         if temple_videos and "null" not in temple_videos:
    #             for video in temple_videos:
    #                 if video and video != "null":
    #                     saved_location = save_video_to_azure(video, serializer.instance._id, serializer.instance.name, entity_type)
    #                     if saved_location:
    #                         saved_videos.append(saved_location)

    #         # Update model with saved image/video paths
    #         if saved_images:
    #             serializer.instance.image_location = saved_images
    #         if saved_videos:
    #             serializer.instance.temple_video = saved_videos
    #         if saved_images or saved_videos:
    #             serializer.instance.save()

    #         # Send Email Notification
    #         created_at = timezone.now()
    #         send_mail(
    #             'New Temple Added',
    #             f'User ID: {request.user.id}\n'
    #             f'Full Name: {request.user.get_full_name()}\n'
    #             f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
    #             f'Temple ID: {serializer.instance._id}\n'
    #             f'Temple Name: {serializer.instance.name}',
    #             settings.EMAIL_HOST_USER,
    #             [settings.EMAIL_HOST_USER],
    #             fail_silently=False,
    #         )

    #         return Response({
    #             "message": "success",
    #             "result": serializer.data
    #         }, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({
    #             "message": "An error occurred.",
    #             "error": str(e)
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def create(self, request, *args, **kwargs):
        try:
            # ----------------------------------
            # Check Authentication
            # ----------------------------------
            if not request.user.is_authenticated:
                return Response(
                    {"message": "Authentication required to submit temple."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ----------------------------------
            # Get Register Instance
            # ----------------------------------
            register_user = get_object_or_404(Register, id=request.user.id)

            # ----------------------------------
            # Handle Image Upload
            # ----------------------------------
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            request.data['image_location'] = "null"

            # ----------------------------------
            # Handle Video Upload
            # ----------------------------------
            temple_videos = request.data.get('temple_video', [])
            if not isinstance(temple_videos, list):
                temple_videos = [temple_videos]
            request.data['temple_video'] = "null"

            # ----------------------------------
            # Save Temple Data (Under Review)
            # ----------------------------------
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=register_user, status="INACTIVE")

            saved_images = []
            saved_videos = []
            entity_type = "temple"

            # ----------------------------------
            # Save Images to Azure
            # ----------------------------------
            for image in image_locations:
                if image and image != "null":
                    saved_location = save_image_to_azure(
                        image,
                        serializer.instance._id,
                        serializer.instance.name,
                        entity_type
                    )
                    if saved_location:
                        saved_images.append(saved_location)

            # ----------------------------------
            # Save Videos to Azure
            # ----------------------------------
            for video in temple_videos:
                if video and video != "null":
                    saved_location = save_video_to_azure(
                        video,
                        serializer.instance._id,
                        serializer.instance.name,
                        entity_type
                    )
                    if saved_location:
                        saved_videos.append(saved_location)

            # ----------------------------------
            # Update Media Fields
            # ----------------------------------
            if saved_images:
                serializer.instance.image_location = saved_images
            if saved_videos:
                serializer.instance.temple_video = saved_videos
            if saved_images or saved_videos:
                serializer.instance.save()

            created_at = timezone.now()

            # ----------------------------------
            # Send Email to Admin
            # ----------------------------------
            send_mail(
                "New Temple Submitted - Under Review",
                f"A new temple has been submitted.\n\n"
                f"User: {register_user.full_name}\n"
                f"Email: {register_user.email}\n"
                f"Temple Name: {serializer.instance.name}\n"
                f"Temple ID: {serializer.instance._id}\n"
                f"Submitted On: {created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ----------------------------------
            # Send Email to User
  
            if register_user.email:

                subject = "Your Temple Submission Is Under Review"

                text_content = f"""
            Dear {register_user.full_name},

            Your temple "{serializer.instance.name}" has been successfully received 
            and is currently under verification.

            Once approved, it will be visible to devotees on the platform.

            Thank you for contributing to Gramadevata.

            Submitted On: {created_at.strftime('%d %B %Y, %I:%M %p')}

            Regards,
            Gramadevata Team
                """

                html_content = f"""
            <div style="font-family: Arial, sans-serif; background:#f4f6f8; padding:30px 0;">
                <div style="max-width:650px; margin:auto; background:#ffffff; 
                            border-radius:8px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.08);">

                    <!-- Header -->
                    <div style="background:#8B0000; color:#ffffff; padding:20px; text-align:center;">
                        <h2 style="margin:0;">Gramadevata</h2>
                        <p style="margin:5px 0 0 0; font-size:14px;">
                            Connecting Devotees with Sacred Places
                        </p>
                    </div>

                    <!-- Body -->
                    <div style="padding:30px; color:#333333;">

                        <h3 style="margin-top:0;">Thank You for Your Contribution 🙏</h3>

                        <p>Dear <strong>{register_user.full_name}</strong>,</p>

                        <p>
                            We are pleased to inform you that your temple 
                            <strong>"{serializer.instance.name}"</strong> 
                            has been successfully received by our team.
                        </p>

                        <p>
                            The submission is currently under review to ensure 
                            all details meet our quality and authenticity standards.
                        </p>

                        <div style="background:#f9fafb; padding:18px; 
                                    border-left:4px solid #8B0000; margin:20px 0;">
                            <p style="margin:0;"><strong>Review Status:</strong> Under Verification ⏳</p>
                            <p style="margin:8px 0 0 0;">
                                <strong>Submitted On:</strong> 
                                {created_at.strftime('%d %B %Y, %I:%M %p')}
                            </p>
                        </div>

                        <p>
                            Once approved, your temple will become visible to devotees 
                            across the platform.
                        </p>

                        <p>
                            We truly appreciate your effort in strengthening 
                            our spiritual community.
                        </p>

                        <!-- Divider -->
                        <hr style="border:none; border-top:1px solid #eeeeee; margin:30px 0;">

                        <p style="font-size:14px; color:#666;">
                            If you have any questions regarding your submission, 
                            feel free to contact our support team.
                        </p>

                        <p style="margin-top:20px;">
                            With sincere gratitude,<br>
                            <strong>Gramadevata Team</strong>
                        </p>
                    </div>

                    <!-- Footer -->
                    <div style="background:#f4f6f8; padding:15px; text-align:center; font-size:12px; color:#777;">
                        © {created_at.year} Gramadevata. All rights reserved.
                    </div>

                </div>
            </div>
                """

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.EMAIL_HOST_USER,
                    [register_user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()



            # ----------------------------------
            # 🔟 Final Response
            # ----------------------------------
            return Response({
                "message": "Temple submitted successfully. Status: INACTIVE (Under Review)",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred while submitting temple.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
  
          # ----------------------------------
        #     if register_user.email:
        #         send_mail(
        #             "Temple Submission Under Review",
        #             f"Dear {register_user.full_name},\n\n"
        #             f"Thank you for submitting your temple "
        #             f"'{serializer.instance.name}'.\n\n"
        #             f"Your temple has been successfully received and is "
        #             f"currently under review by our team.\n\n"
        #             f"Temple ID: {serializer.instance._id}\n"
        #             f"Submitted On: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        #             f"You will be notified once the review process is completed.\n\n"
        #             f"Thank you for your valuable contribution.\n\n"
        #             f"Regards,\nAdmin Team",
        #             settings.EMAIL_HOST_USER,
        #             [register_user.email],
        #             fail_silently=False,
        #         )

        #     return Response({
        #         "message": "success",
        #         "result": serializer.data
        #     }, status=status.HTTP_201_CREATED)

        # except Exception as e:
        #     return Response({
        #         "message": "An error occurred.",
        #         "error": str(e)
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    def retrieve(self, request, pk=None):
        try:
            connect_model = self.get_object()
        except Temple.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TempleDetailSerializer(connect_model)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        try:
            instance = self.get_object()

            # Extract image_location from request data
            image_locations = request.data.get('image_location', [])

            # If image_location is not a list, convert it to a list
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            # Temporarily set image_location to "null"
            request.data['image_location'] = "null"

            # Serialize and update the instance
            serializer = TempleSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            saved_locations = []

            if image_locations and "null" not in image_locations:
                entity_type = "temple"
                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            updated_instance._id,
                            updated_instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)

            if saved_locations:
                updated_instance.image_location = saved_locations
                updated_instance.save()

            updated_time = timezone.now()

            # Send email notification
            send_mail(
                'Temple Updated',
                f'User ID: {request.user.id}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Updated Time: {updated_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Temple ID: {updated_instance._id}\n'
                f'Temple Name: {updated_instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "updated successfully",
                "data": TempleDetailSerializer(updated_instance).data
            })

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

# @method_decorator(cache_page(60 * 5), name='get')  # Cache for 5 minutes
# class GetItemByfield_InputView(generics.GenericAPIView):
#     serializer_class = TempleSerializer1  # Fixed serializer reference

#     def get(self, request, input_value, field_name):
#         try:
#             field_names = [field.name for field in Temple._meta.get_fields()]

#             if field_name in field_names:
#                 filter_kwargs = {field_name: input_value}
#                 queryset = Temple.objects.filter(**filter_kwargs, status='ACTIVE')

#                 serialized_data = TempleSerializer1(
#                     queryset, many=True, context={'request': request}
#                 )
#                 return Response(serialized_data.data)

#             else:
#                 return Response({
#                     'message': 'Invalid field name',
#                     'status': 400
#                 })

#         except Temple.DoesNotExist:
#             return Response({
#                 'message': 'Object not found',
#                 'status': 404
#             })

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.response import Response

# @method_decorator(cache_page(60 * 5), name="get")  # cache 5 min
# class GetItemByfield_InputView(generics.GenericAPIView):
#     serializer_class = TempleSerializer1

#     def get(self, request, input_value, field_name):

#         # validate field name safely
#         valid_fields = {f.name for f in Temple._meta.fields}
#         if field_name not in valid_fields:
#             return Response(
#                 {"message": "Invalid field name", "status": 400},
#                 status=400,
#             )

#         queryset = (
#             Temple.objects
#             .filter(**{field_name: input_value}, status="ACTIVE")
#             # village hierarchy optimization
#             .select_related(
#                 "object_id",
#                 "object_id__block",
#                 "object_id__block__district",
#                 "object_id__block__district__state",
#                 "object_id__block__district__state__country",
#             )
#             # ALL reverse relations used in serializer
#             .prefetch_related(
#                 "Connections",
#                 "favorite",
#                 "visit_temples",
#                 "comments",
#                 "events",
#                 "nearby_hotels",
#                 "tourismplace",
#                 "transport",
#                 "media",
#                 "touroperator",
#                 "social_activity",
#                 "near_by_hospitals",
#                 "temple_facilities",
#                 "prayers_and_benefits",
#                 "tour_guide",
#                 "pooja_timing",
#                 "resturents",
#                 "ambulance_facility",
#                 "blood_bank",
#                 "fire_station",
#                 "police_station",
#                 "pooja_stores",
#                 "goshalas",
#             )
#         )

#         serializer = self.get_serializer(
#             queryset,
#             many=True,
#             context={"request": request}
#         )

#         return Response(serializer.data)

from rest_framework import generics
from rest_framework.response import Response



class GetItemByfield_InputView(generics.GenericAPIView):
    serializer_class = TempleSerializer1

    def get_queryset(self):
        field_name = self.kwargs.get("field_name")
        input_value = self.kwargs.get("input_value")

        # validate field name safely
        valid_fields = {f.name for f in Temple._meta.fields}
        if field_name not in valid_fields:
            return Temple.objects.none()

        return (
            Temple.objects
            .filter(**{field_name: input_value}, status="ACTIVE")
            .select_related(
                "object_id",
                "object_id__block",
                "object_id__block__district",
                "object_id__block__district__state",
                "object_id__block__district__state__country",
            )
            .prefetch_related(
                "Connections",
                "favorite",
                "visit_temples",
                "comments",
                "events",
                "nearby_hotels",
                "tourismplace",
                "transport",
                "media",
                "touroperator",
                "social_activity",
                "near_by_hospitals",
                "temple_facilities",
                "prayers_and_benefits",
                "tour_guide",
                "pooja_timing",
                "resturents",
                "ambulance_facility",
                "blood_bank",
                "fire_station",
                "police_station",
                "pooja_stores",
                "goshalas",
            )
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {"message": "No data found", "status": 404},
                status=404
            )

        serializer = self.get_serializer(
            queryset,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)



# from django.core.cache import cache
# from rest_framework import generics
# from rest_framework.response import Response
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

# class GetItemByfield_InputView(generics.GenericAPIView):
#     serializer_class = TempleSerializer1

#     def get(self, request, input_value, field_name):

#         cache_key = f"temple_detail_{field_name}_{input_value}_{request.user.id if request.user.is_authenticated else 'anon'}"
#         cached_data = cache.get(cache_key)
#         if cached_data:
#             return Response(cached_data)

#         field_names = [f.name for f in Temple._meta.get_fields()]
#         if field_name not in field_names:
#             return Response({"message": "Invalid field name"}, status=400)

#         filter_kwargs = {field_name: input_value}

#         queryset = (
#             Temple.objects
#             .filter(**filter_kwargs, status='ACTIVE')
#             .select_related(
#                 "object_id__block__district__state__country"
#             )
#             .prefetch_related(
#                 "events",
#                 "nearby_hotels",
#                 "tourismplace",
#                 "transport",
#                 "media",
#                 "touroperator",
#                 "social_activity",
#                 "near_by_hospitals",
#                 "temple_facilities",
#                 "prayers_and_benefits",
#                 "tour_guide",
#                 "pooja_timing",
#                 "resturents",
#                 "pooja_stores",
#                 "ambulance_facility",
#                 "blood_bank",
#                 "fire_station",
#                 "police_station",
#                 "Connections",
#                 "favorite",
#                 "visit_temples",
#             )
#         )

#         serializer = TempleSerializer1(
#             queryset,
#             many=True,
#             context={"request": request}
#         )

#         cache.set(cache_key, serializer.data, 300)  # 5 min cache
#         return Response(serializer.data)






class filters_by_iteams(generics.ListAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleSerializer1
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']







from rest_framework import filters



class GetTemplesByLocation(generics.ListAPIView):
    serializer_class = CitySerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]  # Enable search filter
    search_fields = ['name', 'address'] 
    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        if not input_value and not category:
            raise ValidationError("Input value or category is required")

        location_filter = Q()
        if input_value:
            location_filter |= Q(object_id__block__district__state__country__pk=input_value)
            location_filter |= Q(object_id__block__district__state__pk=input_value)
            location_filter |= Q(object_id__block__district__pk=input_value)
            location_filter |= Q(object_id__block__pk=input_value)
            location_filter |= Q(object_id__pk=input_value)

        if category:
            location_filter &= Q(category=category)

        queryset = Temple.objects.filter(location_filter).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id',
        )

        if not queryset.exists() and input_value:
            queryset = Temple.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        if input_value:
            queryset = queryset.order_by('object_id__block__district__state__name')

        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())  # <-- apply filters like search
        queryset = queryset.filter(status='ACTIVE')
        # Annotate with order_priority
        queryset = queryset.annotate(
            order_priority=Case(
                When(priority="d7df749f-97e8-4635-a211-371c44b3c31f", then=0),
                When(priority="630f3239-f515-47fb-be8d-db727b9f2174", then=1),
                When(priority="b78ac28e-d0b5-11ee-84bd-0242ac110002", then=2),
                When(priority="b78ac071-d0b5-11ee-84bd-0242ac110002", then=3),
                default=4,
                output_field=IntegerField()
            )
        )

        # Annotate with order_category
        queryset = queryset.annotate(
            order_category=Case(
                *[
                    When(category_id=cat_id, then=order)
                    for order, cat_id in enumerate([
                        "742ecf7b-d0b5-11ee-84bd-0242ac110002",
                        "742c4b08-d0b5-11ee-84bd-0242ac110002",
                        "742c309e-d0b5-11ee-84bd-0242ac110002",
                        "742c043d-d0b5-11ee-84bd-0242ac110002",
                        "405033fe-fb78-49e0-aef9-35172863466c",
                        "11633522-2084-4f76-b360-0a0038c3f285",
                        "743339d5-d0b5-11ee-84bd-0242ac110002",
                        "74333d89-d0b5-11ee-84bd-0242ac110002",
                        "74333f6a-d0b5-11ee-84bd-0242ac110002",
                        "72524742-6e3a-4c2a-b4d4-4a0a68b5faa7",
                        "957b393b-2198-4e3f-a7a5-61a1b1b9652b",
                        "742f645c-d0b5-11ee-84bd-0242ac110002",
                        "74343760-d0b5-11ee-84bd-0242ac110002",
                        "742f66d4-d0b5-11ee-84bd-0242ac110002",
                        "742ed15f-d0b5-11ee-84bd-0242ac110002",
                        "74353e76-d0b5-11ee-84bd-0242ac110002",
                        "74334755-d0b5-11ee-84bd-0242ac110002",
                        "742fb823-d0b5-11ee-84bd-0242ac110002",
                        "7434333a-d0b5-11ee-84bd-0242ac110002",
                        "7433a0e7-d0b5-11ee-84bd-0242ac110002",
                        "74344055-d0b5-11ee-84bd-0242ac110002",
                        "742ecbf6-d0b5-11ee-84bd-0242ac110002",
                        "742e85ad-d0b5-11ee-84bd-0242ac110002",
                        "74345ef3-d0b5-11ee-84bd-0242ac110002",
                        "74353c0d-d0b5-11ee-84bd-0242ac110002",
                        "742ed999-d0b5-11ee-84bd-0242ac110002",
                        "742b10a6-d0b5-11ee-84bd-0242ac110002",
                        "742da6dc-d0b5-11ee-84bd-0242ac110002",
                        "742f57d9-d0b5-11ee-84bd-0242ac110002",
                        "74344b60-d0b5-11ee-84bd-0242ac110002",
                        "742c8632-d0b5-11ee-84bd-0242ac110002",
                        "742ee33e-d0b5-11ee-84bd-0242ac110002",
                        "742ccfe6-d0b5-11ee-84bd-0242ac110002",
                        "742cc4f8-d0b5-11ee-84bd-0242ac110002",
                        "742c5302-d0b5-11ee-84bd-0242ac110002",
                        "742da3d3-d0b5-11ee-84bd-0242ac110002",
                        "742f52be-d0b5-11ee-84bd-0242ac110002",
                        "74339dc3-d0b5-11ee-84bd-0242ac110002",
                        "743525d3-d0b5-11ee-84bd-0242ac110002",
                        "742f2965-d0b5-11ee-84bd-0242ac110002",
                        "742c0c1b-d0b5-11ee-84bd-0242ac110002",
                        "742c1781-d0b5-11ee-84bd-0242ac110002",
                        "742ebd7b-d0b5-11ee-84bd-0242ac110002",
                        "fee05763-b9b1-49d5-8423-b385625045ff",
                        "743340c9-d0b5-11ee-84bd-0242ac110002",
                        "a19958cc-86c2-44fc-a8f2-35c54208fae5",
                        "742fc433-d0b5-11ee-84bd-0242ac110002",
                        "05dd3bfa-8f5a-49f7-83de-520a3b1c012d",
                        "4117b4f9-f202-4b10-a637-50fc5151a0e4",
                        "2257a2c4-73ac-49c1-ba3d-376c10b0c664",
                        "6af7ab24-9a0e-42cb-a57a-372bc62cd842",
                        "142a703b-e8ad-4550-b68a-6a0718b90922",
                        "49eabde2-ce67-426a-a0ad-e51849910401",
                        "d4f979f4-2f7a-4aab-9782-702b31a21087",
                        "742fc5ca-d0b5-11ee-84bd-0242ac110002",
                        "6af7ab24-9a0e-42cb-a57a-372bc62cd842",
                    ])
                ],
                default=55,
                output_field=IntegerField()
            )
        )

        # Final ordering (without alphabetical state name)
        queryset = queryset.order_by('order_category', 'order_priority')

        category = request.query_params.get('category')
        no_pagination_categories = [
            "74343760-d0b5-11ee-84bd-0242ac110002",
            "405033fe-fb78-49e0-aef9-35172863466c",
        ]

        if category and category in no_pagination_categories:
            serializer = CitySerializer(queryset, many=True)
            return Response({
                "count": queryset.count(),
                "next": None,
                "previous": None,
                "results": serializer.data
            })

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CitySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)





class Templepost(generics.CreateAPIView):
    serializer_class = TempleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        try:
            # Fetch the Register instance for the logged-in user using the username
            username = request.user.username  # Example: Using username
            print(f"Username: {username}")
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member
            print(f"is_member: {is_member}")

            # Check if the user is a member
            if is_member == "NO":
                print("User is not a member")
                return Response({
                    "message": "Cannot add the temple. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Register.DoesNotExist:
            return Response({
                "message": "User not found in Register."
            }, status=status.HTTP_404_NOT_FOUND)

        # Extract image_location from request data
        image_location = request.data.get('image_location')

        # Add the image_location back to the request data
        request.data['image_location'] = "null"

        # Serialize data and save
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        if image_location and image_location != "null":
            saved_location = save_image_to_folder(image_location, serializer.instance._id, serializer.instance.name)
            print(saved_location, "=================================")
            if saved_location:
                serializer.instance.image_location = saved_location
                serializer.instance.save()

        return Response({
            "message": "success",
            "result": serializer.data
        })


class TempleDetailView(generics.RetrieveAPIView):
    queryset = Temple.objects.all()
    serializer_class = TempleDetailSerializer

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        try:
            temple = self.get_object()
            serializer = self.get_serializer(temple)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Temple.DoesNotExist:
            return Response({"error": "Temple not found"}, status=status.HTTP_404_NOT_FOUND)



class GetbyCountryLocationTemples(generics.ListAPIView):
    serializer_class = TempleSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        country_id = self.kwargs.get('country_id')
        temples_in_country = Temple.objects.filter(
            object_id__block__district__state__country_id=country_id
        )
        return temples_in_country




    
class GetItemByfield_location(generics.ListAPIView):
    serializer_class = TempleSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        temples_in_state = Temple.objects.filter(object_id__block__district__state_id=state_id)
        return temples_in_state
    
class GetbyDistrictLocationTemples(generics.ListAPIView):
    serializer_class = TempleSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        temples_in_district = Temple.objects.filter(object_id__block__district_id=district_id)
        return temples_in_district
    


    
class GetbyBlockLocationTemples(generics.ListAPIView):
    serializer_class = TempleSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        block_id = self.kwargs.get('block_id')
        temples_in_district = Temple.objects.filter(object_id__block_id=block_id)
        return temples_in_district

    


        

    


    

from rest_framework.pagination import PageNumberPagination

class GetIndianTemples(APIView):

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    

    def get(self, request):
        indian_location = Village.objects.all()
        temple_query_set = Temple.objects.all()
        indian_temples = temple_query_set.filter(object_id__in=indian_location)
       


        paginator = PageNumberPagination()
        paginator.page_size = 50 
        indian_temples_page = paginator.paginate_queryset(indian_temples, request)


        indiantemples = TempleSerializer1(indian_temples_page, many=True)
        
        return paginator.get_paginated_response( indiantemples.data)
    

from rest_framework.pagination import PageNumberPagination

class GetGlobalTemples(APIView):

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    
    def get(self, request):
        temple_query_set = Temple.objects.all()
        global_temples = temple_query_set.exclude(geo_site__in=['S', 'D', 'B', 'V'])

        paginator = PageNumberPagination()
        paginator.page_size = 50 
        global_temples_page = paginator.paginate_queryset(global_temples, request)

        globaltemples = TempleSerializer1(global_temples_page, many=True)

        return paginator.get_paginated_response( globaltemples.data)

from rest_framework.generics import GenericAPIView


    
      
class InactiveTempleAPIView(GenericAPIView):
    """API to get only INACTIVE temples"""

    queryset = Temple.objects.filter(status='INACTIVE').order_by('-created_at')
    serializer_class = InactiveTempleSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'location']


    filter_backends = [DjangoFilterBackend, SearchFilter]  
    search_fields = ['name', 'location'] 

    def get(self, request):
        queryset = Temple.objects.filter(status='INACTIVE')
        search_query = request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)  # Replace with the correct field
            )
 # Priority IDs
        Main = "d7df749f-97e8-4635-a211-371c44b3c31f"
        Famous = "630f3239-f515-47fb-be8d-db727b9f2174"
        Highest = "b782cfa1-d0b5-11ee-84bd-0242ac110002"
        Medium = "b78ac28e-d0b5-11ee-84bd-0242ac110002"
        Lowest = "b78ac071-d0b5-11ee-84bd-0242ac110002"
        # Annotate and Order by Priority IDs
        queryset = queryset.annotate(
        order_priority=Case(
        When(priority__name="Main", then=0),
        When(priority__name="Famous", then=1),
        When(priority__name="Highest", then=2),
        When(priority__name="Medium", then=3),
        When(priority__name="Lowest", then=4),
        default=5,
        output_field=IntegerField()
    )
    ).order_by('order_priority')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = InactiveTempleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = InactiveTempleSerializer(queryset, many=True)
        return Response(serializer.data)















       


class GetInactiveTempleByFieldView(generics.GenericAPIView):
    serializer_class = TempleSerializer1


    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Temple._meta.get_fields()]

            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Temple.objects.filter(**filter_kwargs, status='INACTIVE')
                
                # ✅ Pass request into serializer context
                serialized_data = TempleDetailSerializer(queryset, many=True, context={'request': request})

                return Response(serialized_data.data)

            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })

        except Temple.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })






from uuid import UUID




 






class GetInactiveTemplesByLocation(generics.ListAPIView):
    serializer_class = InactiveTempleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        if not input_value and not category:
            raise ValidationError("Input value or category is required")

        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        combined_query = Q()

        if input_value:
            combined_query |= (
                country_query |
                state_query |
                district_query |
                block_query |
                village_query
            )

        if category:
            combined_query &= Q(category=category)

        queryset = Temple.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id'
        )

        # Fallback direct object_id filter
        if not queryset.exists() and input_value:
            queryset = Temple.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='INACTIVE').order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = InactiveTempleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = InactiveTempleSerializer(queryset, many=True)
        return Response(serializer.data)





@method_decorator(cache_page(60 * 5), name='dispatch')  # 5 minutes cache
class GetTownTemplesByLocation(APIView):
    def get(self, request):
        input_value = request.query_params.get('input_value')
        search_query = request.query_params.get('search', '')

        if not input_value:
            raise ValidationError("Location input_value is required")

        iconic_id = UUID("d7df749f-97e8-4635-a211-371c44b3c31f")
        famous_id = UUID("630f3239-f515-47fb-be8d-db727b9f2174")
        gramadevata_id = UUID("742ccfe6-d0b5-11ee-84bd-0242ac110002")

        temple_filter = Q(status='ACTIVE')
        geo_data = {}

        def parse_images(image_str):
            if not image_str:
                return []
            try:
                image_list = json.loads(image_str)
            except Exception:
                cleaned_str = image_str.strip('[]"\'')
                image_list = [img.strip().strip('"').strip("'") for img in cleaned_str.split(',') if img.strip()]
            base_url = "https://sathayushstorage.blob.core.windows.net/sathayush/"
            return [base_url + img.replace("\\", "/").lstrip('/') for img in image_list]

        # Determine location
        try:
            village = Village.objects.select_related('block__district__state__country').get(pk=input_value)
            temple_filter &= Q(object_id=village)
            geo_data = {
                "village_images": parse_images(village.image_location),
                "village_desc": village.desc,
                "village": village.name,
                "block": village.block.name,
                "district": village.block.district.name,
                "state": village.block.district.state.name,
                "country": village.block.district.state.country.name
            }
            location_type = 'village'
            location_instance = village
        except Village.DoesNotExist:
            try:
                block = Block.objects.select_related('district__state__country').get(pk=input_value)
                temple_filter &= Q(object_id__block=block)
                geo_data = {
                    "block_images": parse_images(block.image_location),
                    "block_desc": block.desc,
                    "block": block.name,
                    "district": block.district.name,
                    "state": block.district.state.name,
                    "country": block.district.state.country.name
                }
                location_type = 'block'
                location_instance = block
            except Block.DoesNotExist:
                raise ValidationError("No village or block found for given input_value")

        if search_query:
            temple_filter &= Q(name__icontains=search_query) | Q(address__icontains=search_query)

        all_temples = Temple.objects.filter(temple_filter)

        # Categorization
        iconic_temples = all_temples.filter(priority=iconic_id)
        famous_temples = all_temples.filter(priority=famous_id)
        gramadevata_temples = all_temples.filter(category=gramadevata_id)

        excluded_ids = list(iconic_temples.values_list('_id', flat=True)) + \
                       list(famous_temples.values_list('_id', flat=True)) + \
                       list(gramadevata_temples.values_list('_id', flat=True))

        other_temples = all_temples.exclude(_id__in=excluded_ids)
        all_ids = list(all_temples.values_list('_id', flat=True))

        # ✅ Determine village_ids for linked data
        if location_type == 'village':
            village_ids = [location_instance._id]
        elif location_type == 'block':
            village_ids = list(Village.objects.filter(block=location_instance).values_list('_id', flat=True))
        else:
            village_ids = []

        # Related data
        events = Event.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        goshalas = Goshala.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        facilities = TempleFacilities.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        guides = TourGuide.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        hospitals = NearbyHospital.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        hotels = TempleNearbyHotel.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        activities = SocialActivity.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        transports = TempleTransport.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        tour_operators = TourOperator.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        tourism_places = TempleNearbyTourismPlace.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        # ✅ Emergency services by both temple and village
        police_station = PoliceStation.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        ambulance_facility = AmbulanceFacility.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        fire_station = FireStation.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        blood_bank = BloodBank.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        welfare_homes = WelfareHomes.objects.filter(
            village_id__in=village_ids,
            status='ACTIVE'
        ).distinct()

        # Independent (block/village) based
        independent_events = Event.objects.filter(object_id__block__pk=input_value, status='ACTIVE')
        independent_goshalas = Goshala.objects.filter(object_id__block__pk=input_value, status='ACTIVE')
        resturants = TempleNearbyRestaurant.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        return Response({
            "location_details": geo_data,
            "temples": CitySerializer1(all_temples, many=True).data,
            "iconic_temples": CitySerializer1(iconic_temples, many=True).data,
            "famous_temples": CitySerializer1(famous_temples, many=True).data,
            "gramadevata_temples": CitySerializer1(gramadevata_temples, many=True).data,
            "other_temples": CitySerializer1(other_temples, many=True).data,
            "events": TownSerializers1(events | independent_events, many=True).data,
            "goshalas": StateSerializer1(goshalas | independent_goshalas, many=True).data,
            "temple_facilities": TempleFacilitiesSerializer(facilities, many=True).data,
            "temple_guides": TourGuideSerializer(guides, many=True).data,
            "nearby_hospitals": NearbyHospitalSerializer1(hospitals, many=True).data,
            "nearby_hotels": TempleNearbyHotelSerializer1(hotels, many=True).data,
            "nearby_resturants": TempleNearbyRestaurantSerializer1(resturants, many=True).data,
            "social_activities": SocialActivitySerializer(activities, many=True).data,
            "nearby_tourism_places": TourismPlacelocationSerializer(tourism_places, many=True).data,
            "temple_transport": TempleTransportSerializer(transports, many=True).data,
            "tour_operators": TourOperatorSerializer(tour_operators, many=True).data,
            "police_station": PoliceStationSerializer1(police_station, many=True).data,
            "ambulance_facility": AmbulanceFacilitySerializer1(ambulance_facility, many=True).data,
            "fire_station": FireStationSerializer1(fire_station, many=True).data,
            "blood_bank": BloodBankSerializer1(blood_bank, many=True).data,
            "welfare_homes": WelfareHomeslocationSerializer(welfare_homes, many=True).data,
        })





@method_decorator(cache_page(60 * 5), name='dispatch')  # Cache for 5 minutes
class GetCityTemplesByLocation(APIView):

    def get(self, request):
        input_value = request.query_params.get('input_value')
        search_text = request.query_params.get('search', '').strip()

        if not input_value:
            raise ValidationError("Location input_value is required")

        # UUIDs for priority categories
        iconic_id = UUID("d7df749f-97e8-4635-a211-371c44b3c31f")
        famous_id = UUID("630f3239-f515-47fb-be8d-db727b9f2174")
        gramadevata_id = UUID("742ccfe6-d0b5-11ee-84bd-0242ac110002")

        temple_filter = Q(status='ACTIVE')
        geo_data = {}
        location_type = None
        location_instance = None

        def parse_images(image_str):
            if not image_str:
                return []
            try:
                image_list = json.loads(image_str)
            except Exception:
                cleaned_str = image_str.strip('[]"\'')
                image_list = [img.strip().strip('"').strip("'") for img in cleaned_str.split(',') if img.strip()]
            base_url = "https://sathayushstorage.blob.core.windows.net/sathayush/"
            return [base_url + img.replace("\\", "/").lstrip('/') for img in image_list]

        # Location resolution
        try:
            village = Village.objects.select_related('block__district__state__country').get(pk=input_value)
            temple_filter &= Q(object_id=village)
            geo_data = {
                "village_images": parse_images(village.image_location),
                "village_desc": village.desc,
                "village": village.name,
                "block": village.block.name,
                "district": village.block.district.name,
                "state": village.block.district.state.name,
                "country": village.block.district.state.country.name
            }
            location_type = 'village'
            location_instance = village

        except Village.DoesNotExist:
            try:
                block = Block.objects.select_related('district__state__country').get(pk=input_value)
                temple_filter &= Q(object_id__block=block)
                geo_data = {
                    "block_images": parse_images(block.image_location),
                    "block_desc": block.desc,
                    "block": block.name,
                    "district": block.district.name,
                    "state": block.district.state.name,
                    "country": block.district.state.country.name
                }
                location_type = 'block'
                location_instance = block

            except Block.DoesNotExist:
                try:
                    district = District.objects.select_related('state__country').get(pk=input_value)
                    temple_filter &= Q(object_id__block__district=district)
                    geo_data = {
                        "district_images": parse_images(district.image_location),
                        "district_desc": district.desc,
                        "district": district.name,
                        "state": district.state.name,
                        "country": district.state.country.name
                    }
                    location_type = 'district'
                    location_instance = district

                except District.DoesNotExist:
                    raise ValidationError("No village, block, or district found for given input_value")

        # Fetch temples
        all_temples = Temple.objects.filter(temple_filter)

        if search_text:
            search_filter = Q(name__icontains=search_text) | Q(address__icontains=search_text)
            all_temples = all_temples.filter(search_filter)

        iconic_temples = all_temples.filter(priority=iconic_id)
        famous_temples = all_temples.filter(priority=famous_id)
        gramadevata_temples = all_temples.filter(category=gramadevata_id)

        excluded_ids = list(iconic_temples.values_list('_id', flat=True)) + \
                       list(famous_temples.values_list('_id', flat=True)) + \
                       list(gramadevata_temples.values_list('_id', flat=True))

        other_temples = all_temples.exclude(_id__in=excluded_ids)
        all_ids = all_temples.values_list('_id', flat=True)

        # Determine village IDs based on location
        village_ids = []
        if location_type == 'village':
            village_ids = [location_instance._id]
        elif location_type == 'block':
            village_ids = Village.objects.filter(block=location_instance).values_list('_id', flat=True)
        elif location_type == 'district':
            village_ids = Village.objects.filter(block__district=location_instance).values_list('_id', flat=True)

        # Fetch related data
        events = Event.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        goshalas = Goshala.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        facilities = TempleFacilities.objects.filter(temple_id__in=all_ids, status='ACTIVE')
        guides = TourGuide.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        hospitals = NearbyHospital.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        hotels = TempleNearbyHotel.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        activities = SocialActivity.objects.filter(temple_id__in=all_ids, status='ACTIVE')

        # ✅ FIXED: Include tourism places by both temple and village ID
        tourism_places = TempleNearbyTourismPlace.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        transports = TempleTransport.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        tour_operators = TourOperator.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        prayers_and_benefits = PrayersAndBenefits.objects.filter(temple_id__in=all_ids, status='ACTIVE')

        # Independent data
        independent_events = Event.objects.filter(object_id__block__pk=input_value, status='ACTIVE')
        independent_goshalas = Goshala.objects.filter(object_id__block__pk=input_value, status='ACTIVE')

        # Restaurants
        resturants = TempleNearbyRestaurant.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        # Emergency services
        police_station = PoliceStation.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        ambulance_facility = AmbulanceFacility.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'  
        ).distinct()
        fire_station = FireStation.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()
        blood_bank = BloodBank.objects.filter(
            Q(temple_id__in=all_ids) | Q(village_id__in=village_ids),
            status='ACTIVE'
        ).distinct()

        welfare_homes = WelfareHomes.objects.filter(
            village_id__in=village_ids,
            status='ACTIVE'
        ).distinct()

        return Response({
            "location_details": geo_data,
            "temples": CitySerializer1(all_temples, many=True).data,
            "iconic_temples": CitySerializer1(iconic_temples, many=True).data,
            "famous_temples": CitySerializer1(famous_temples, many=True).data,
            "gramadevata_temples": CitySerializer1(gramadevata_temples, many=True).data,
            "other_temples": CitySerializer1(other_temples, many=True).data,
            "events": TownSerializers1(events | independent_events, many=True).data,
            "goshalas": StateSerializer1(goshalas | independent_goshalas, many=True).data,
            "temple_facilities": TempleFacilitiesSerializer(facilities, many=True).data,
            "temple_guides": TourGuideSerializer(guides, many=True).data,
            "nearby_hospitals": NearbyHospitalSerializer1(hospitals, many=True).data,
            "nearby_hotels": TempleNearbyHotelSerializer1(hotels, many=True).data,
            "nearby_resturants": TempleNearbyRestaurantSerializer1(resturants, many=True).data,
            "social_activities": SocialActivitySerializer(activities, many=True).data,
            "nearby_tourism_places": TourismPlacelocationSerializer(tourism_places, many=True).data,
            "temple_transport": TempleTransportSerializer(transports, many=True).data,
            "tour_operators": TourOperatorSerializer(tour_operators, many=True).data,
            "police_station": PoliceStationSerializer1(police_station, many=True).data,
            "ambulance_facility": AmbulanceFacilitySerializer1(ambulance_facility, many=True).data,
            "fire_station": FireStationSerializer1(fire_station, many=True).data,
            "blood_bank": BloodBankSerializer1(blood_bank, many=True).data,
            "welfare_homes": WelfareHomeslocationSerializer(welfare_homes, many=True).data,
        })






from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
import json



from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100




from django.db.models import Q, Case, When, Value, IntegerField





@method_decorator(cache_page(300), name='get')
class GetStateTemplesByLocation(APIView):

    def parse_images(self, image_str):
        if not image_str:
            return []
        try:
            image_list = json.loads(image_str)
        except Exception:
            image_list = image_str.strip('[]"\'').split(',')
            image_list = [img.strip().strip('"').strip("'") for img in image_list if img.strip()]
        base_url = settings.FILE_URL
        return [base_url + img.replace("\\", "/").lstrip('/') for img in image_list]

    def get_location_geo_data(self, input_value):
        try:
            state = State.objects.select_related('country').get(pk=input_value)
            return {
                "type": "state",
                "geo": {
                    "state": state.name,
                    "state_desc": state.desc or "",
                    "state_images": self.parse_images(state.image_location),
                    "country": state.country.name if state.country else "Unknown Country",
                },
                "filter": Q(object_id__block__district__state=state),
                "object": state
            }
        except State.DoesNotExist:
            pass

        try:
            district = District.objects.select_related('state__country').get(pk=input_value)
            return {
                "type": "district",
                "geo": {
                    "district": district.name,
                    "district_desc": district.desc or "",
                    "district_images": self.parse_images(district.image_location),
                    "state": district.state.name,
                    "country": district.state.country.name if district.state.country else "Unknown Country",
                },
                "filter": Q(object_id__block__district=district),
                "object": district
            }
        except District.DoesNotExist:
            pass

        try:
            block = Block.objects.select_related('district__state__country').get(pk=input_value)
            return {
                "type": "block",
                "geo": {
                    "block": block.name,
                    "block_desc": block.desc or "",
                    "block_images": self.parse_images(block.image_location),
                    "district": block.district.name,
                    "state": block.district.state.name,
                    "country": block.district.state.country.name if block.district.state.country else "Unknown Country",
                },
                "filter": Q(object_id__block=block),
                "object": block
            }
        except Block.DoesNotExist:
            pass

        try:
            village = Village.objects.select_related('block__district__state__country').get(pk=input_value)
            return {
                "type": "village",
                "geo": {
                    "village": village.name,
                    "village_desc": village.desc or "",
                    "village_images": self.parse_images(village.image_location),
                    "block": village.block.name,
                    "district": village.block.district.name,
                    "state": village.block.district.state.name,
                    "country": village.block.district.state.country.name if village.block.district.state.country else "Unknown Country",
                },
                "filter": Q(object_id=village),
                "object": village
            }
        except Village.DoesNotExist:
            pass

        raise ValidationError("Invalid input_value. No matching location found.")

    def get(self, request):
        input_value = request.query_params.get('input_value')
        search_query = request.query_params.get('search', '')

        if not input_value:
            raise ValidationError("Location input_value is required")

        location_data = self.get_location_geo_data(input_value)
        temple_filter = Q(status='ACTIVE') & location_data['filter']

        if search_query:
            search_filter = Q(name__icontains=search_query) | Q(address__icontains=search_query)
            temple_filter &= search_filter

        temples = Temple.objects.filter(temple_filter)

        # Priority and Category IDs
        ICONIC_TEMPLE_ID = "d7df749f-97e8-4635-a211-371c44b3c31f"
        FAMOUS_TEMPLE_ID = "630f3239-f515-47fb-be8d-db727b9f2174"
        GRAMADEVATA_CATEGORY_ID = "742ccfe6-d0b5-11ee-84bd-0242ac110002"

        # Special reorder condition
        SPECIAL_TEMPLE_ID = "c7cf23c3-82c1-409f-9726-840693a3ffe0"
        ANDHRA_PRADESH_STATE_ID = "d1b01400-d0b0-11ee-ade9-0242ac110002"

        iconic_queryset = temples.filter(priority_id=ICONIC_TEMPLE_ID)

        if input_value == ANDHRA_PRADESH_STATE_ID:
            iconic = iconic_queryset.annotate(
                custom_order=Case(
                    When(pk=SPECIAL_TEMPLE_ID, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('custom_order', 'name')
        else:
            iconic = iconic_queryset.order_by('name')

        famous = temples.filter(priority_id=FAMOUS_TEMPLE_ID).order_by('name')
        gramadevata = temples.filter(category_id=GRAMADEVATA_CATEGORY_ID).exclude(
            priority_id__in=[ICONIC_TEMPLE_ID, FAMOUS_TEMPLE_ID]
        ).order_by('name')
        other = temples.exclude(category_id=GRAMADEVATA_CATEGORY_ID).exclude(
            priority_id__in=[ICONIC_TEMPLE_ID, FAMOUS_TEMPLE_ID]
        ).order_by('name')

        paginator = CustomPagination()
        paginated_famous = paginator.paginate_queryset(famous, request)
        paginated_gramadevata = paginator.paginate_queryset(gramadevata, request)
        paginated_other = paginator.paginate_queryset(other, request)

        temple_ids = temples.values_list("_id", flat=True)
        village_ids = []

        loc_type = location_data["type"]
        loc_obj = location_data["object"]

        if loc_type == "village":
            village_ids = [loc_obj._id]
        elif loc_type == "block":
            village_ids = Village.objects.filter(block=loc_obj).values_list("_id", flat=True)
        elif loc_type == "district":
            village_ids = Village.objects.filter(block__district=loc_obj).values_list("_id", flat=True)
        elif loc_type == "state":
            village_ids = Village.objects.filter(block__district__state=loc_obj).values_list("_id", flat=True)

        # ✅ Fixed: Get tourism places based on temple_id or village_id
        tourism_places = TempleNearbyTourismPlace.objects.filter(
            Q(temple_id__in=temple_ids) | Q(village_id__in=village_ids),
            status="ACTIVE"
        ).distinct()

        events = Event.objects.filter(status='ACTIVE').filter(location_data['filter'])
        goshalas = Goshala.objects.filter(status='ACTIVE').filter(location_data['filter'])
        welfare_homes = WelfareHomes.objects.filter(
            village_id__in=village_ids,
            status='ACTIVE'
        ).distinct()

        return paginator.get_paginated_response({
            "location_details": location_data['geo'],
            "iconic_temples": CitySerializer1(iconic, many=True).data,
            "famous_temples": CitySerializer1(paginated_famous, many=True).data,
            "gramadevata_temples": CitySerializer1(paginated_gramadevata, many=True).data,
            "other_temples": CitySerializer1(paginated_other, many=True).data,
            "events": TownSerializers1(events, many=True).data,
            "goshalas": StateSerializer1(goshalas, many=True).data,
            "nearby_tourism_places": TourismPlacelocationSerializer(tourism_places, many=True).data,
            "welfare_homes": WelfareHomeslocationSerializer(welfare_homes, many=True).data,
        })