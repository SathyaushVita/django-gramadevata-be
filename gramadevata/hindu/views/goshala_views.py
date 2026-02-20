
from ..serializers import GoshalaSerializer,GoshalaSerializer1,CitySerializer,GoshalaLocationSerializer,GoshalaInactiveSerializer
from ..models import Goshala,Register,Event
from rest_framework import viewsets
from rest_framework .response import Response
from ..utils import save_image_to_folder, CustomPagination,save_image_to_azure,save_image_to_azure1
from rest_framework.views import APIView
from .village_views import Village
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework import generics,status
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404

from ..utils import save_video_to_azure
from uuid import UUID
from ..models import Temple

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import ValidationError








class GoshalaView(viewsets.ModelViewSet):
    queryset = Goshala.objects.all()
    serializer_class = GoshalaSerializer

        
    def list(self, request):
            filter_kwargs = {key: value for key, value in request.query_params.items()}
            queryset = Goshala.objects.filter(status='ACTIVE', **filter_kwargs)

            if not queryset.exists():
                return Response({'message': 'Data not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

            iconic_id = UUID("d7df749f-97e8-4635-a211-371c44b3c31f")
            famous_id = UUID("630f3239-f515-47fb-be8d-db727b9f2174")
            gramadevata_id = UUID("742ccfe6-d0b5-11ee-84bd-0242ac110002")

            final_data = []

            for goshala in queryset:
                village = goshala.object_id
                block = village.block if village else None

                base_queryset = Temple.objects.all()
                if village:
                    base_queryset = base_queryset.filter(object_id=village)
                elif block:
                    base_queryset = base_queryset.filter(object_id__block=block)

                iconic_temples = base_queryset.filter(priority=iconic_id)
                famous_temples = base_queryset.filter(priority=famous_id)
                gramadevata_temples = base_queryset.filter(category=gramadevata_id)

                exclude_ids = set(
                    list(iconic_temples.values_list('pk', flat=True)) +
                    list(famous_temples.values_list('pk', flat=True)) +
                    list(gramadevata_temples.values_list('pk', flat=True))
                )
                other_temples = base_queryset.exclude(pk__in=exclude_ids)

                # -------- Nearby Events Logic -------- #
                event_queryset = Event.objects.all()
                if village:
                    event_queryset = event_queryset.filter(object_id=village)
                elif block:
                    event_queryset = event_queryset.filter(object_id__block=block)

                serialized_events = CitySerializer(event_queryset, many=True, context={'request': request})
                # ------------------------------------- #

                serialized_goshala = GoshalaSerializer1(goshala, context={'request': request})
                serialized_iconic = CitySerializer(iconic_temples, many=True, context={'request': request})
                serialized_famous = CitySerializer(famous_temples, many=True, context={'request': request})
                serialized_gramadevata = CitySerializer(gramadevata_temples, many=True, context={'request': request})
                serialized_others = CitySerializer(other_temples, many=True, context={'request': request})

                data = serialized_goshala.data
                data['nearby_temples'] = {
                    "iconic_temples": serialized_iconic.data,
                    "famous_temples": serialized_famous.data,
                    "gramadevata_temples": serialized_gramadevata.data,
                    "other_temples": serialized_others.data,
                }

                # Add nearby events to response
                data['nearby_events'] = serialized_events.data

                final_data.append(data)

            return Response(final_data, status=status.HTTP_200_OK)

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
                return Response({
                    "message": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)

            if register_instance.is_member == "false":
                return Response({
                    "message": "Cannot add Goshala. Membership details are required. Update your profile and become a member to add Goshala."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Extract files
            image_location = request.data.get('image_location', [])
            goshala_video = request.data.get('goshala_video', [])

            if not isinstance(image_location, list):
                image_location = [image_location]
            if not isinstance(goshala_video, list):
                goshala_video = [goshala_video]

            request.data['image_location'] = "null"
            request.data['goshala_video'] = "null"

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            instance = serializer.instance

            saved_images = []
            saved_videos = []

            entity_type = "Goshala"

            # Save Images
            for img_loc in image_location:
                if img_loc and img_loc != "null":
                    location = save_image_to_azure1(
                        img_loc,
                        instance._id,
                        instance.name,
                        entity_type
                    )
                    if location:
                        saved_images.append(location)

            # Save Videos
            for video_loc in goshala_video:
                if video_loc and video_loc != "null":
                    video_url = save_video_to_azure(
                        video_loc,
                        instance._id,
                        instance.name,
                        entity_type
                    )
                    if video_url:
                        saved_videos.append(video_url)

            if saved_images:
                instance.image_location = saved_images
            if saved_videos:
                instance.goshala_video = saved_videos

            instance.save()

            created_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            # ==================================
            # ✅ Email to Admin
            # ==================================
            send_mail(
                'New Goshala Added',
                f'User ID: {request.user.id}\n'
                f'User Name: {register_instance.full_name}\n'
                f'Created Time: {created_at}\n'
                f'Goshala ID: {instance._id}\n'
                f'Goshala Name: {instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ==================================
            # ✅ Email to User
            # ==================================
            if register_instance.email:
                send_mail(
                    'Goshala Submission Received - Under Review',
                    f'Dear {register_instance.full_name},\n\n'
                    f'Thank you for submitting the Goshala "{instance.name}".\n'
                    f'Your submission has been successfully received and is currently under review.\n\n'
                    f'We will notify you once it is approved.\n\n'
                    f"Thank you for your valuable contribution.\n\n"
                    f'Regards,\n'
                    f'Gramadevata Admin Team',
                    settings.EMAIL_HOST_USER,
                    [register_instance.email],
                    fail_silently=False,
                )

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    # def create(self, request, *args, **kwargs):
    #     try:
    #         email = getattr(request.user, 'email', None)
    #         contact_number = getattr(request.user, 'contact_number', None)

    #         # Attempt to find the Register instance by either email or contact number
    #         register_instance = None
    #         if email:
    #             register_instance = Register.objects.filter(email=email).first()
    #         elif contact_number:
    #             register_instance = Register.objects.filter(contact_number=contact_number).first()

    #         # If no user found, return error
    #         if not register_instance:
    #             return Response({
    #                 "message": "User not found."
    #             }, status=status.HTTP_404_NOT_FOUND)

    #         # Check membership status
    #         is_member = register_instance.is_member
    #         if is_member == "false":
    #             return Response({
    #                 "message": "Cannot add Goshala. Membership details are required. Update your profile and become a member to add Temple."
    #             }, status=status.HTTP_400_BAD_REQUEST)

    #         # Extract image_location and goshala_video from request data
    #         image_location = request.data.get('image_location', [])
    #         goshala_video = request.data.get('goshala_video', [])

    #         if not isinstance(image_location, list):
    #             image_location = [image_location]
    #         if not isinstance(goshala_video, list):
    #             goshala_video = [goshala_video]

    #         request.data['image_location'] = "null"
    #         request.data['goshala_video'] = "null"

    #         # Serialize data and save
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         saved_images = []
    #         saved_videos = []

    #         entity_type = "Goshala"

    #         # Save images to Azure
    #         if image_location and "null" not in image_location:
    #             for img_loc in image_location:
    #                 if img_loc and img_loc != "null":
    #                     single_saved_location = save_image_to_azure1(
    #                         img_loc,
    #                         serializer.instance._id,
    #                         serializer.instance.name,
    #                         entity_type
    #                     )
    #                     if single_saved_location:
    #                         saved_images.append(single_saved_location)

    #         # Save videos to Azure
    #         if goshala_video and "null" not in goshala_video:
    #             for video_loc in goshala_video:
    #                 if video_loc and video_loc != "null":
    #                     single_saved_location = save_video_to_azure(
    #                         video_loc,
    #                         serializer.instance._id,
    #                         serializer.instance.name,
    #                         entity_type
    #                     )
    #                     if single_saved_location:
    #                         saved_videos.append(single_saved_location)

    #         # Update model with saved image/video paths
    #         if saved_images:
    #             serializer.instance.image_location = saved_images
    #         if saved_videos:
    #             serializer.instance.goshala_video = saved_videos
    #         if saved_images or saved_videos:
    #             serializer.instance.save()

    #         # Capture the current time
    #         created_at = timezone.now()

    #         # Send email to EMAIL_HOST_USER
    #         send_mail(
    #             'New Goshala Added',
    #             f'User ID: {request.user.id}\n'
    #             f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
    #             f'Goshala ID: {serializer.instance._id}\n'
    #             f'Goshala Name: {serializer.instance.name}',
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






    def retrieve(self, request, pk=None):
            try:
                goshala = self.get_object()
            except Goshala.DoesNotExist:
                return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
            village = goshala.object_id
            block = village.block if village else None
            iconic_id = UUID("d7df749f-97e8-4635-a211-371c44b3c31f")
            famous_id = UUID("630f3239-f515-47fb-be8d-db727b9f2174")
            # area_village_ids = [
            #     UUID("b78ac071-d0b5-11ee-84bd-0242ac110002"),
            #     UUID("b78ac28e-d0b5-11ee-84bd-0242ac110002")
            # ]
            gramadevata_id = UUID("742ccfe6-d0b5-11ee-84bd-0242ac110002")  # Your actual gramadevata category id
            # Base queryset of temples related to this goshala's location (village or block)
            base_queryset = Temple.objects.all()
            if village:
                base_queryset = base_queryset.filter(object_id=village)
            elif block:
                base_queryset = base_queryset.filter(object_id__block=block)
            # Filter temples by priority / category sets
            iconic_temples = base_queryset.filter(priority=iconic_id)
            famous_temples = base_queryset.filter(priority=famous_id)
            # area_village_temples = base_queryset.filter(object_id__in=area_village_ids)
            gramadevata_temples = base_queryset.filter(category=gramadevata_id)
            # Exclude above from others
            exclude_ids = set(
                list(iconic_temples.values_list('pk', flat=True)) +
                list(famous_temples.values_list('pk', flat=True)) +
                # list(area_village_temples.values_list('pk', flat=True)) +
                list(gramadevata_temples.values_list('pk', flat=True))
            )
            other_temples = base_queryset.exclude(pk__in=exclude_ids)
            # Serialize
            serialized_goshala = GoshalaSerializer1(goshala, context={'request': request})
            serialized_iconic = CitySerializer(iconic_temples, many=True, context={'request': request})
            serialized_famous = CitySerializer(famous_temples, many=True, context={'request': request})
            # serialized_area_village = TempleMiniSerializer(area_village_temples, many=True, context={'request': request})
            serialized_gramadevata = CitySerializer(gramadevata_temples, many=True, context={'request': request})
            serialized_others = CitySerializer(other_temples, many=True, context={'request': request})
            data = serialized_goshala.data
            data['nearby_temples'] = {
                "iconic_temples": serialized_iconic.data,
                "famous_temples": serialized_famous.data,
                # "area_village_temples": serialized_area_village.data,
                "gramadevata_temples": serialized_gramadevata.data,
                "other_temples": serialized_others.data,
            }
            return Response(data)

     
    def update(self, request, pk=None):
        try:
            # Find the register instance from email or contact number
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            register_instance = None
            if email:
                register_instance = Register.objects.filter(email=email).first()
            elif contact_number:
                register_instance = Register.objects.filter(contact_number=contact_number).first()

            if not register_instance:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Membership check
            if register_instance.is_member == "false":
                return Response({
                    "message": "Cannot update Goshala. Membership details are required. Update your profile and become a member to update Goshala."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get instance to update
            instance = self.get_object()

            # Extract image_location
            image_location = request.data.get('image_location', [])
            if not isinstance(image_location, list):
                image_location = [image_location]

            # Temporarily set image_location to "null" for validation
            request.data['image_location'] = "null"

            # Validate and save the data
            serializer = GoshalaSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()

            saved_location = []

            if image_location and "null" not in image_location:
                entity_type = "Goshala"
                for img_loc in image_location:
                    if img_loc and img_loc != "null":
                        single_saved_location = save_image_to_azure(
                            img_loc,
                            updated_instance._id,
                            updated_instance.name,
                            entity_type
                        )
                        if single_saved_location:
                            saved_location.append(single_saved_location)

            if saved_location:
                updated_instance.image_location = saved_location
                updated_instance.save()

            updated_time = timezone.now()

            # Send email notification
            send_mail(
                'Goshala Updated',
                f'User ID: {request.user.id}\n'
                # f'Full Name: {request.user.get_full_name()}\n'
                f'Updated Time: {updated_time.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Goshala ID: {updated_instance._id}\n'
                f'Goshala Name: {updated_instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "updated successfully",
                "data": GoshalaSerializer1(updated_instance).data
            })

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class GhoshalaPost(generics.CreateAPIView):
    serializer_class = GoshalaSerializer
    # permission_classes = [IsAuthenticated]
    
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        try:
           
            username = request.user.username  
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






@method_decorator(cache_page(300), name='list')  # Caches the list method for 5 minutes
class GetGoshalasByLocation(generics.ListAPIView):
    serializer_class = GoshalaLocationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        if not input_value and not category:
            raise ValidationError("Input value or category is required")

        # Define queries for each level correctly
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Combine queries
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        if category:
            combined_query &= Q(category=category)

        queryset = Goshala.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id',
        )

        if not queryset.exists():
            queryset = Goshala.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)






class GetGlobalGoshalas(APIView):

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    def get(self, request):
        Event_query_set = Goshala.objects.all()
        global_goshala = Event_query_set.exclude(geo_site__in=['S', 'D', 'B', 'V'])

        paginator = PageNumberPagination()
        paginator.page_size = 50 
        global_goshalas_page = paginator.paginate_queryset(global_goshala, request)

        globalevents = GoshalaSerializer1(global_goshalas_page, many=True)

        return paginator.get_paginated_response( globalevents.data)      



class GetIndianGoshalas(APIView):

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def get(self, request):
        indian_location = Village.objects.all()
        temple_query_set = Goshala.objects.all()
        indian_temples = temple_query_set.filter(object_id__in=indian_location)
       


        paginator = PageNumberPagination()
        paginator.page_size = 50 
        indian_goshala_page = paginator.paginate_queryset(indian_temples, request)


        indiangoshalas = GoshalaSerializer1(indian_goshala_page, many=True)
        
        return paginator.get_paginated_response( indiangoshalas.data)
    

class GetbyStateLocationGoshalas(generics.ListAPIView):
    serializer_class = GoshalaSerializer1

    # permission_classes = []
    
    # def get_permissions(self):
    #     if self.request.method in ['GET', 'POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        temples_in_state = Goshala.objects.filter(object_id__block__district__state_id=state_id)
        return temples_in_state
    
class GetbyDistrictLocationGoshalas(generics.ListAPIView):
    serializer_class = GoshalaSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        temples_in_district = Goshala.objects.filter(object_id__block__district_id=district_id)
        return temples_in_district
    


    
class GetbyBlockLocationGoshalas(generics.ListAPIView):
    serializer_class = GoshalaSerializer1

    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        block_id = self.kwargs.get('block_id')
        temples_in_district = Goshala.objects.filter(object_id__block_id=block_id)
        return temples_in_district
    








class InactiveGoshalaAPIView(APIView):
    """API to get only INACTIVE goshala records"""

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None) 

        for key, value in request.query_params.items():
            if key != 'search':  
                filter_kwargs[key] = value

        queryset = Goshala.objects.filter(status='INACTIVE', **filter_kwargs)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response({'message': 'Data not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = GoshalaInactiveSerializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'goshala': serialized_data.data
        }, status=status.HTTP_200_OK)





class GetInactiveGoshalaByFieldView(generics.GenericAPIView):
    serializer_class = GoshalaSerializer1
    # permission_classes = []

    # def get_permissions(self):
    #     if self.request.method in ['GET', 'POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def get(self, request, input_value, field_name):
        try:
            # Get all field names in the Goshala model
            field_names = [field.name for field in Goshala._meta.get_fields()]

            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Goshala.objects.filter(**filter_kwargs, status='INACTIVE')

                if not queryset.exists():
                    return Response({'message': 'Data not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

                serializer = GoshalaSerializer1(queryset, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response({
                    'message': f"Invalid field name: '{field_name}'",
                    'status': 400
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'message': 'Something went wrong',
                'error': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)











class GetInactiveGoshalasByLocation(generics.ListAPIView):
    serializer_class = GoshalaInactiveSerializer
    pagination_class = CustomPagination



    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        if not input_value and not category:
            raise ValidationError("Input value or category is required")

        # Define queries for each level correctly
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Combine queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)

        queryset = Goshala.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id',

            # 'object_id__district__state__country',
            # 'object_id__district__state',
            # 'object_id__district',
            # 'object_id',

            # 'object_id__state__country',
            # 'object_i__state',
            # 'object_id',

            # 'object_id__country',
            # 'object_id'
        )

        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists():
            queryset = Goshala.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

        return queryset

    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().filter(status='INACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)












