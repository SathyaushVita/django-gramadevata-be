
from ..serializers import *
from ..models import *
from rest_framework import viewsets
from rest_framework .response import Response
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from ..utils import save_image_to_folder,CustomPagination, save_image_to_azure,save_video_to_azure
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from ..enums import EventStatusEnum
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from uuid import UUID
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class EventView(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            email = getattr(user, 'email', None)
            contact_number = getattr(user, 'contact_number', None)

            # Get Register instance
            register_instance = Register.objects.filter(
                email=email
            ).first() or Register.objects.filter(
                contact_number=contact_number
            ).first()

            if not register_instance:
                return Response(
                    {"message": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if register_instance.is_member == "false":
                return Response({
                    "message": "Cannot add Event. Membership required. Update your profile and become a member to add an event."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Extract file fields safely
            image_locations = request.data.pop('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]

            event_videos = request.data.pop('event_video', [])
            if not isinstance(event_videos, list):
                event_videos = [event_videos]

            request.data['image_location'] = []
            request.data['event_video'] = []

            # Save event initially
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance = serializer.instance

            # Save images
            saved_locations = []
            for img in image_locations:
                if img and img != "null":
                    location = save_image_to_azure(
                        img,
                        instance._id,
                        instance.name,
                        "events"
                    )
                    if location:
                        saved_locations.append(location)

            # Save videos
            saved_videos = []
            for vid in event_videos:
                if vid and vid != "null":
                    video_url = save_video_to_azure(
                        vid,
                        instance._id,
                        instance.name,
                        "events"
                    )
                    if video_url:
                        saved_videos.append(video_url)

            if saved_locations:
                instance.image_location = saved_locations

            if saved_videos:
                instance.event_video = saved_videos

            # Update status
            instance.update_event_status()
            instance.save()

            created_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            # ===============================
            # ✅ Email to Admin
            # ===============================
            send_mail(
                'New Event Added',
                f'User ID: {user.id}\n'
                f'User Name: {register_instance.full_name}\n'
                f'Created Time: {created_time}\n'
                f'Event ID: {instance._id}\n'
                f'Event Name: {instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ===============================
            # ✅ Email to User
            # ===============================
            if register_instance.email:
                send_mail(
                    'Event Submission Received - Under Review',
                    f'Dear {register_instance.full_name},\n\n'
                    f'Thank you for submitting your event "{instance.name}".\n'
                    f'Your event has been successfully received and is currently under review.\n\n'
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
                "result": self.get_serializer(instance).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def create(self, request, *args, **kwargs):
    #             try:
    #                 user = request.user
    #                 email = getattr(user, 'email', None)
    #                 contact_number = getattr(user, 'contact_number', None)
    #                 # Get the Register instance using email or contact_number
    #                 register_instance = Register.objects.filter(
    #                     email=email
    #                 ).first() or Register.objects.filter(contact_number=contact_number).first()
    #                 if not register_instance:
    #                     return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    #                 if register_instance.is_member == "false":
    #                     return Response({
    #                         "message": "Cannot add Event. Membership required. Update your profile and become a member to add an event."
    #                     }, status=status.HTTP_400_BAD_REQUEST)
    #                 # Extract file fields safely
    #                 image_locations = request.data.pop('image_location', [])
    #                 if not isinstance(image_locations, list):
    #                     image_locations = [image_locations]
    #                 event_videos = request.data.pop('event_video', [])
    #                 if not isinstance(event_videos, list):
    #                     event_videos = [event_videos]
    #                 # Temporarily set placeholders for image/video fields
    #                 request.data['image_location'] = []
    #                 request.data['event_video'] = []
    #                 # Save event initially
    #                 serializer = self.get_serializer(data=request.data)
    #                 serializer.is_valid(raise_exception=True)
    #                 serializer.save()
    #                 instance = serializer.instance
    #                 saved_locations = []
    #                 for img in image_locations:
    #                     if img and img != "null":
    #                         location = save_image_to_azure(img, instance._id, instance.name, "events")
    #                         if location:
    #                             saved_locations.append(location)
    #                 saved_videos = []
    #                 for vid in event_videos:
    #                     if vid and vid != "null":
    #                         video_url = save_video_to_azure(vid, instance._id, instance.name, "events")
    #                         if video_url:
    #                             saved_videos.append(video_url)
    #                 if saved_locations:
    #                     instance.image_location = saved_locations
    #                 if saved_videos:
    #                     instance.event_video = saved_videos
    #                 # :white_check_mark: Update the event status here
    #                 instance.update_event_status()
    #                 # Save everything
    #                 instance.save()
    #                 # Email notification
    #                 send_mail(
    #                     'New Event Added',
    #                     f'User ID: {user.id}\n'
    #                     f'Created Time: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    #                     f'Event ID: {instance._id}\n'
    #                     f'Event Name: {instance.name}',
    #                     settings.EMAIL_HOST_USER,
    #                     [settings.EMAIL_HOST_USER],
    #                     fail_silently=False,
    #                 )
    #                 return Response({
    #                     "message": "success",
    #                     "result": self.get_serializer(instance).data
    #                 }, status=status.HTTP_201_CREATED)
    #             except Exception as e:
    #                 return Response({
    #                     "message": "An error occurred.",
    #                     "error": str(e)
    #                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






    def list(self, request):
            ICONIC_ID = UUID("d7df749f-97e8-4635-a211-371c44b3c31f")
            FAMOUS_ID = UUID("630f3239-f515-47fb-be8d-db727b9f2174")
            GRAMADEVATA_ID = UUID("742ccfe6-d0b5-11ee-84bd-0242ac110002")

            filter_kwargs = {key: value for key, value in request.query_params.items()}
            queryset = Event.objects.filter(status='ACTIVE', **filter_kwargs)

            if not queryset.exists():
                return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)

            for event in queryset:
                event.update_event_status()

            queryset = Event.objects.filter(status='ACTIVE', **filter_kwargs)

            def enrich_events(events):
                enriched = []
                for event in events:
                    village = event.object_id
                    block = village.block if village else None

                    temples_qs = Temple.objects.all()
                    if village:
                        temples_qs = temples_qs.filter(object_id=village)
                    elif block:
                        temples_qs = temples_qs.filter(object_id__block=block)

                    iconic_temples = temples_qs.filter(priority=ICONIC_ID)
                    famous_temples = temples_qs.filter(priority=FAMOUS_ID)
                    gramadevata_temples = temples_qs.filter(category=GRAMADEVATA_ID)

                    exclude_ids = set(
                        list(iconic_temples.values_list('_id', flat=True)) +
                        list(famous_temples.values_list('_id', flat=True)) +
                        list(gramadevata_temples.values_list('_id', flat=True))
                    )
                    other_temples = temples_qs.exclude(_id__in=exclude_ids)

                    event_data = EventSerializer1(event, context={'request': request}).data
                    event_data['nearby_temples'] = {
                        "iconic_temples": CitySerializer(iconic_temples, many=True, context={'request': request}).data,
                        "famous_temples": CitySerializer(famous_temples, many=True, context={'request': request}).data,
                        "gramadevata_temples": CitySerializer(gramadevata_temples, many=True, context={'request': request}).data,
                        "other_temples": CitySerializer(other_temples, many=True, context={'request': request}).data,
                    }
                    enriched.append(event_data)
                return enriched

            # ✅ Case 1: If no query parameters (get all events)
            if not filter_kwargs:
                all_events = Event.objects.filter(status='ACTIVE')
                for event in all_events:
                    event.update_event_status()
                all_events = Event.objects.filter(status='ACTIVE')

                upcoming = all_events.filter(event_status=EventStatusEnum.UPCOMING.name)
                ongoing = all_events.filter(event_status=EventStatusEnum.ONGOING.name)
                completed = all_events.filter(event_status=EventStatusEnum.COMPLETED.name)

                return Response({
                    "status": 200,
                    "event_upcoming": enrich_events(upcoming),
                    "event_ongoing": enrich_events(ongoing),
                    "event_completed": enrich_events(completed),
                })

            # ✅ Case 2: If query params exist (e.g., ?id=...)
            return Response(enrich_events(queryset), status=status.HTTP_200_OK)



        


    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
        except Event.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer1(instance)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        try:
            email = getattr(request.user, 'email', None)
            contact_number = getattr(request.user, 'contact_number', None)

            # Attempt to find the Register instance
            register_instance = None
            if email:
                register_instance = Register.objects.filter(email=email).first()
            elif contact_number:
                register_instance = Register.objects.filter(contact_number=contact_number).first()

            if not register_instance:
                return Response({
                    "message": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)

            # Check membership
            if register_instance.is_member == "false":
                return Response({
                    "message": "Cannot update Event. Membership details are required. Update your profile and become a member to update Event."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Get instance
            instance = self.get_object()

            # Handle image upload
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            request.data['image_location'] = "null"  # Set to "null" before serializing

            # Serialize and save
            serializer = EventSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_locations = []
            if image_locations and "null" not in image_locations:
                entity_type = "events"
                for image_location in image_locations:
                    if image_location and image_location != "null":
                        saved_location = save_image_to_azure(
                            image_location,
                            serializer.instance._id,
                            serializer.instance.name,
                            entity_type
                        )
                        if saved_location:
                            saved_locations.append(saved_location)
            if saved_locations:
                serializer.instance.image_location = saved_locations
                serializer.instance.save()

            # Send email notification
            updated_at = timezone.now()
            send_mail(
                'Event Updated',
                f'User ID: {request.user.id}\n'
                f'Updated Time: {updated_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Event ID: {serializer.instance._id}\n'
                f'Event Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "updated successfully",
                "data": EventSerializer1(serializer.instance).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class EventPost(generics.CreateAPIView):
    serializer_class = EventSerializer
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








@method_decorator(cache_page(300), name='list')  # cache the list method for 5 minutes
class GetEventsByLocation(generics.ListAPIView):
    serializer_class = EventLocationSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")

        today = timezone.now().date()

        # Define queries for each location level
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)

        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query

        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)

        # Filter by date and order
        queryset = Event.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),
                When(start_date__lt=today, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )

        # Fallback if empty
        if not queryset.exists() and input_value:
            queryset = Event.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),
                    When(start_date__lt=today, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)

        if page is not None:
            upcoming_events = queryset.filter(event_status="UPCOMING")
            completed_events = queryset.filter(event_status="COMPLETED")
            ongoing_events = queryset.filter(event_status="ONGOING")

            return Response({
                "status": 200,
                "event_upcoming": self.get_serializer(upcoming_events, many=True).data,
                "event_completed": self.get_serializer(completed_events, many=True).data,
                "event_ongoing": self.get_serializer(ongoing_events, many=True).data,
            })

        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        ongoing_events = queryset.filter(event_status="ONGOING")

        return Response({
            "status": 200,
            "event_upcoming": self.get_serializer(upcoming_events, many=True).data,
            "event_completed": self.get_serializer(completed_events, many=True).data,
            "event_ongoing": self.get_serializer(ongoing_events, many=True).data,
        })




class GetIndianEvents(APIView):
    def get(self, request):
        indian_location = Village.objects.all()
        event_query_set = Event.objects.all()
        indian_Events = event_query_set.filter(object_id__in=indian_location)
       


        paginator = PageNumberPagination()
        paginator.page_size = 50 
        indian_events_page = paginator.paginate_queryset(indian_Events, request)


        indianevents = EventSerializer1(indian_events_page, many=True)
        
        return paginator.get_paginated_response( indianevents.data)
        


class GetGlobalEvents(APIView):
    def get(self, request):
        Event_query_set = Event.objects.all()
        global_events = Event_query_set.exclude(geo_site__in=['S', 'D', 'B', 'V'])

        paginator = PageNumberPagination()
        paginator.page_size = 50 
        global_temples_page = paginator.paginate_queryset(global_events, request)

        globalevents = EventSerializer1(global_temples_page, many=True)

        return paginator.get_paginated_response( globalevents.data)


class GetbyStateLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        temples_in_state = Event.objects.filter(object_id__block__district__state_id=state_id)
        return temples_in_state
    
class GetbyDistrictLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        temples_in_district = Event.objects.filter(object_id__block__district_id=district_id)
        return temples_in_district
    

   
class GetbyBlockLocationEvents(generics.ListAPIView):
    serializer_class = EventSerializer1

    def get_queryset(self):
        block_id = self.kwargs.get('block_id')
        temples_in_district = Event.objects.filter(object_id__block_id=block_id)
        return temples_in_district
    










class EventstatusView(generics.ListAPIView):
    serializer_class = EventSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        now = timezone.now()

        queryset = Event.objects.all()

        # Update event statuses before returning the queryset
        for event in queryset:
            event.update_event_status()

        if status_param:
            if status_param not in dict(EventStatusEnum.__members__).keys():
                raise ValidationError("Invalid status value")
            queryset = queryset.filter(event_status=status_param)

        # Order events: upcoming events first, then completed events
        return queryset.order_by(
            Case(
                When(event_status=EventStatusEnum.UPCOMING.name, then=Value(0)),
                When(event_status=EventStatusEnum.COMPLETED.name, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'  # Further order by start date within each status group
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



























from rest_framework.viewsets import ViewSet


class EventInactiveViewSet(APIView):
    
    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)  # Search parameter

        # Collect filter params dynamically
        for key, value in request.query_params.items():
            if key != 'search': 
                filter_kwargs[key] = value

        queryset = Event.objects.filter(status='INACTIVE', **filter_kwargs)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )

        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response({'message': 'Data not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        ongoing_events = queryset.filter(event_status="ONGOING")

        event_upcoming_serializer = EventInactiveSerializer(upcoming_events, many=True)
        event_completed_serializer = EventInactiveSerializer(completed_events, many=True)
        event_ongoing_serializer = EventInactiveSerializer(ongoing_events, many=True)

        return Response({
            "count": queryset.count(),  
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
            "event_ongoing": event_ongoing_serializer.data
        }, status=status.HTTP_200_OK)









    
class GetInactiveEventByFieldView(generics.GenericAPIView):
    serializer_class = EventSerializer1


    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Event._meta.get_fields()]

            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Event.objects.filter(**filter_kwargs, status='INACTIVE')

                if not queryset.exists():
                    return Response({'message': 'Event not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

                serializer = EventSerializer1(queryset, many=True, context={'request': request})
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
        









class GetInactiveEventsByLocation(generics.ListAPIView):
    serializer_class = EventInactiveSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")
        today = timezone.now().date()
        # Define queries for each location level
        country_query = Q(object_id__block__district__state__country__pk=input_value)
        state_query = Q(object_id__block__district__state__pk=input_value)
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)
        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |= country_query | state_query | district_query | block_query | village_query
        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)
        # Filter by proximity to today's date and order by start date
        queryset = Event.objects.filter(combined_query).select_related(
            'object_id__block__district__state__country',
            'object_id__block__district__state',
            'object_id__block__district',
            'object_id__block',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                When(start_date__lt=today, then=Value(1)),   # Past events
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )
        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists() and input_value:
            queryset = Event.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)
            # Reorder by proximity to today's date and start date
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                    When(start_date__lt=today, then=Value(1)),   # Past events
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )
        return queryset
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().filter(status='INACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Filter for upcoming and completed events
            upcoming_events = queryset.filter(event_status="UPCOMING")
            completed_events = queryset.filter(event_status="COMPLETED")
            event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
            event_completed_serializer = self.get_serializer(completed_events, many=True)
            return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })
        serializer = self.get_serializer(queryset, many=True)
        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)
        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })










class GetCityEventsByLocation(generics.ListAPIView):
    serializer_class = CityEventSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")
        today = timezone.now().date()
        # Define queries for each location level
        district_query = Q(object_id__block__district__pk=input_value)
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)
        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |=  district_query | block_query | village_query
        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)
        # Filter by proximity to today's date and order by start date
        queryset = Event.objects.filter(combined_query).select_related(
            'object_id__block__district',
            'object_id__block',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                When(start_date__lt=today, then=Value(1)),   # Past events
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )
        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists() and input_value:
            queryset = Event.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)
            # Reorder by proximity to today's date and start date
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                    When(start_date__lt=today, then=Value(1)),   # Past events
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )
        return queryset
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Filter for upcoming and completed events
            upcoming_events = queryset.filter(event_status="UPCOMING")
            completed_events = queryset.filter(event_status="COMPLETED")
            event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
            event_completed_serializer = self.get_serializer(completed_events, many=True)
            return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })
        serializer = self.get_serializer(queryset, many=True)
        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)
        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })







class GetTownEventsByLocation(generics.ListAPIView):
    serializer_class = CityEventSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')
        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")
        today = timezone.now().date()
        # Define queries for each location level
        block_query = Q(object_id__block__pk=input_value)
        village_query = Q(object_id__pk=input_value)
        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |=  block_query | village_query
        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)
        # Filter by proximity to today's date and order by start date
        queryset = Event.objects.filter(combined_query).select_related(
            'object_id__block',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                When(start_date__lt=today, then=Value(1)),   # Past events
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )
        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists() and input_value:
            queryset = Event.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)
            # Reorder by proximity to today's date and start date
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                    When(start_date__lt=today, then=Value(1)),   # Past events
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )
        return queryset
    def list(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        queryset = self.get_queryset().filter(status='ACTIVE')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Filter for upcoming and completed events
            upcoming_events = queryset.filter(event_status="UPCOMING")
            completed_events = queryset.filter(event_status="COMPLETED")
            event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
            event_completed_serializer = self.get_serializer(completed_events, many=True)
            return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })
        serializer = self.get_serializer(queryset, many=True)
        upcoming_events = queryset.filter(event_status="UPCOMING")
        completed_events = queryset.filter(event_status="COMPLETED")
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)
        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })

