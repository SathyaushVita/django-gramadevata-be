from ..serializers import *
from ..models import Village
from rest_framework import viewsets,status
from rest_framework .response import Response
from ..utils import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from ..utils import save_image_to_folder,send_email, send_mail,save_image_to_azure,save_video_to_azure,save_image_to_azure1
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from django.core.cache import cache
from django.db.models import Case, When, Value, IntegerField
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from ..serializers import VillageSerializer3
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from rest_framework import generics
from ..serializers import VillageSerializer 
from rest_framework.filters import SearchFilter







@method_decorator(cache_page(60 * 5), name="dispatch")
class VillageView(viewsets.ModelViewSet):
    queryset = Village.objects.all()
    serializer_class = VillageSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Village.objects.filter(status="ACTIVE")
        params = self.request.query_params.dict()

        params.pop("page", None)
        params.pop("page_size", None)

        if params:
            queryset = queryset.filter(**params)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset:
            return Response({
                "message": "Data not found",
                "status": 404
            })

        serializer = VillageSearchSerializer(queryset, many=True)
        return Response(serializer.data)       

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)




    def create(self, request, *args, **kwargs):
        try:
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            request.data['image_location'] = "null"

            village_videos = request.data.get('village_video', [])
            if not isinstance(village_videos, list):
                village_videos = [village_videos]
            request.data['village_video'] = "null"

            serializer = VillageSerializer2(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            instance = serializer.instance
            entity_type = "village"

            saved_images = []
            saved_videos = []

            for image in image_locations:
                if image and image != "null":
                    location = save_image_to_azure1(
                        image, instance._id, instance.name, entity_type
                    )
                    if location:
                        saved_images.append(location)

            for video in village_videos:
                if video and video != "null":
                    location = save_video_to_azure(
                        video, instance._id, instance.name, entity_type
                    )
                    if location:
                        saved_videos.append(location)

            if saved_images:
                instance.image_location = saved_images
            if saved_videos:
                instance.village_video = saved_videos

            instance.save()

            created_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            # ===============================
            # ✅ Email to Admin
            # ===============================
            send_mail(
                'New Village Added',
                f'User ID: {request.user.id}\n'
                f'Created Time: {created_time}\n'
                f'Village ID: {instance._id}\n'
                f'Village Name: {instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # ===============================
            # ✅ Email to User
            # ===============================
            user_email = getattr(request.user, 'email', None)
            user_name = getattr(request.user, 'full_name', 'User')

            if user_email:
                send_mail(
                    'Village Submission Successful',
                    f'Dear {user_name},\n\n'
                    f'Your village "{instance.name}" has been successfully submitted.\n\n'
                    f"currently under review by our team.\n\n"
                    f"You will be notified once the review process is completed.\n\n"
                    f"Thank you for your valuable contribution.\n\n"
                    f'Regards,\n'
                    f'Gramadevata Admin Team',
                    settings.EMAIL_HOST_USER,
                    [user_email],
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
    #         # Handle image upload
    #         image_locations = request.data.get('image_location', [])
    #         if not isinstance(image_locations, list):
    #             image_locations = [image_locations]
    #         request.data['image_location'] = "null"

    #         # Handle video upload
    #         village_videos = request.data.get('village_video', [])
    #         if not isinstance(village_videos, list):
    #             village_videos = [village_videos]
    #         request.data['village_video'] = "null"

    #         # Save main village data
    #         serializer = VillageSerializer2(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         saved_images = []
    #         saved_videos = []
    #         entity_type = "village"

    #         # Save images to Azure
    #         if image_locations and "null" not in image_locations:
    #             for image in image_locations:
    #                 if image and image != "null":
    #                     saved_location = save_image_to_azure1(
    #                         image, serializer.instance._id, serializer.instance.name, entity_type
    #                     )
    #                     if saved_location:
    #                         saved_images.append(saved_location)

    #         # Save videos to Azure
    #         if village_videos and "null" not in village_videos:
    #             for video in village_videos:
    #                 if video and video != "null":
    #                     saved_location = save_video_to_azure(
    #                         video, serializer.instance._id, serializer.instance.name, entity_type
    #                     )
    #                     if saved_location:
    #                         saved_videos.append(saved_location)

    #         # Update model with saved paths
    #         if saved_images:
    #             serializer.instance.image_location = saved_images
    #         if saved_videos:
    #             serializer.instance.village_video = saved_videos
    #         if saved_images or saved_videos:
    #             serializer.instance.save()

    #         return Response({
    #             "message": "success",
    #             "result": serializer.data
    #         }, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({
    #             "message": "An error occurred.",
    #             "error": str(e)
    #         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Village, pk=kwargs.get('pk'))

            # Handle image upload
            image_locations = request.data.get('image_location', [])
            if not isinstance(image_locations, list):
                image_locations = [image_locations]
            request.data['image_location'] = "null"

            # Handle video upload
            village_videos = request.data.get('village_video', [])
            if not isinstance(village_videos, list):
                village_videos = [village_videos]
            request.data['village_video'] = "null"

            # Save village updates
            serializer = VillageSerializer2(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            saved_images = []
            saved_videos = []
            entity_type = "village"

            # Save images to Azure
            if image_locations and "null" not in image_locations:
                for image in image_locations:
                    if image and image != "null":
                        saved_location = save_image_to_azure(
                            image, instance._id, instance.name, entity_type
                        )
                        if saved_location:
                            saved_images.append(saved_location)

            # Save videos to Azure
            if village_videos and "null" not in village_videos:
                for video in village_videos:
                    if video and video != "null":
                        saved_location = save_video_to_azure(
                            video, instance._id, instance.name, entity_type
                        )
                        if saved_location:
                            saved_videos.append(saved_location)

            # Update model with saved paths
            if saved_images:
                instance.image_location = saved_images
            if saved_videos:
                instance.village_video = saved_videos
            if saved_images or saved_videos:
                instance.save()

            return Response({
                "message": "success",
                "result": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "message": "An error occurred during update.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










class GetVillages(viewsets.ModelViewSet):
    queryset = Village.objects.all().filter(status='ACTIVE')
    serializer_class = VillageSerializer
    pagination_class = CustomPagination
    permission_classes = []
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', ]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = VillageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = VillageSerializer(queryset, many=True)
        return Response(serializer.data)




@api_view(['GET'])
def search_village(request):
    village_name = request.GET.get('village_name')
    country_id = request.GET.get('country_id')
    state_id = request.GET.get('state_id')
    district_id = request.GET.get('district_id')
    
    # Base query with exact match on village name
    base_query = Q(name__iexact=village_name)

    # Apply filters based on user input
    if country_id:
        base_query &= Q(block__district__state__country__pk=country_id)
    if state_id:
        base_query &= Q(block__district__state__pk=state_id)
    if district_id:
        base_query &= Q(block__district__pk=district_id)

    # Retrieve the villages based on the current filters
    villages = Village.objects.filter(base_query).select_related(
        'block__district__state__country'
    )

    # Count the exact matches and proceed based on result counts
    exact_match_count = villages.count()

    # If there are more than 10 exact matches without country filter, prompt to select country
    if exact_match_count > 10 and not country_id:
        countries = Village.objects.filter(name__iexact=village_name).values(
            'block__district__state__country__pk', 'block__district__state__country__name'
        ).distinct()
        return Response({
            "message": "There are more than 10 exact matches. Please narrow your search by selecting a country.",
            "countries": list(countries)
        })

    # If there are still more than 10 exact matches after selecting country, prompt to select state
    if exact_match_count > 10 and not state_id:
        states = Village.objects.filter(
            name__iexact=village_name, block__district__state__country__pk=country_id
        ).values('block__district__state__pk', 'block__district__state__name').distinct()
        return Response({
            "message": "There are more than 10 exact matches. Please narrow your search by selecting a state.",
            "states": list(states)
        })

    # If there are still more than 10 exact matches after selecting state, prompt to select district
    if exact_match_count > 10 and not district_id:
        districts = Village.objects.filter(
            name__iexact=village_name, 
            block__district__state__country__pk=country_id,
            block__district__state__pk=state_id
        ).values('block__district__pk', 'block__district__name').distinct()
        return Response({
            "message": "There are more than 10 exact matches. Please narrow your search by selecting a district.",
            "districts": list(districts)
        })

    # If the matches are 10 or fewer after filtering, return the results
    serializer = VillageSearchSerializer(villages, many=True)
    return Response(serializer.data)



from rest_framework.views import APIView


class InactiveVillageAPIView(APIView):
    """API to get only INACTIVE villages with optional search by name"""

    def get(self, request):
        filter_kwargs = {}
        search_query = request.query_params.get('search', None)

        # Add other query params as filters dynamically (excluding 'search')
        for key, value in request.query_params.items():
            if key != 'search':
                filter_kwargs[key] = value

        # Base queryset: inactive villages
        queryset = Village.objects.filter(**filter_kwargs, status='INACTIVE')\
                                  .select_related('user')

        # Apply search only on village name
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Order by most recent first
        queryset = queryset.order_by('-created_at')

        if not queryset.exists():
            return Response({'message': 'Data not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = VillageSerializer2(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'villages': serialized_data.data
        }, status=status.HTTP_200_OK)

        



from rest_framework import generics, status



class GetInactiveVillageByFieldView(generics.GenericAPIView):
    serializer_class = VillageSerializer
    # permission_classes = []

    # def get_permissions(self):
    #     if self.request.method in ['GET', 'POST', 'PUT']:
    #         return [IsAuthenticated()]
    #     return super().get_permissions()

    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Village._meta.get_fields()]

            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Village.objects.filter(**filter_kwargs, status='INACTIVE')

                if not queryset.exists():
                    return Response({'message': 'Village not found', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

                serializer = VillageSerializer(queryset, many=True, context={'request': request})
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








class FastPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })

from django.core.cache import cache
from django.db.models import Case, When, Value, IntegerField
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import Village
from ..serializers import VillageSerializer3

class GetVillagesByLocation(generics.ListAPIView):
    serializer_class = VillageSerializer2
    pagination_class = FastPagination

    def get_queryset(self):
        input_value = self.request.query_params.get("input_value")
        search = self.request.query_params.get("search", "").strip()

        if not input_value:
            raise ValidationError("input_value is required")

        # ✅ LOCATION FILTER (country / state / district / block)
        location_filter = (
            Q(block__district__state__country__pk=input_value) |
            Q(block__district__state__pk=input_value) |
            Q(block__district__pk=input_value) |
            Q(block__pk=input_value)
        )

        qs = Village.objects.filter(
            location_filter,
            status="ACTIVE"
        ).only(
            "_id", "name", "image_location", "block_id", "precedence"
        )

        # 🔍 SEARCH
        if search:
            if len(search) >= 4:
                qs = qs.extra(
                    where=["MATCH(village.name) AGAINST (%s IN BOOLEAN MODE)"],
                    params=[f"{search}*"]
                )
            else:
                qs = qs.filter(name__icontains=search)

        # ⭐ PRECEDENCE SORTING
        qs = qs.annotate(
            safe_precedence=Case(
                When(precedence__isnull=True, then=Value(9999)),
                When(precedence=0, then=Value(9999)),
                default="precedence",
                output_field=IntegerField()
            )
        )

        return qs.order_by("safe_precedence", "name")

    def list(self, request, *args, **kwargs):
        cache_key = f"villages:fast:{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 600)
        return Response(response.data)



from django.http import JsonResponse
from rest_framework.views import APIView
import json
import re
from ..models import Temple, Goshala, Village, TempleNearbyTourismPlace, Event
class ShareContentView(APIView):
    def get_model_and_url(self, content_type):
        mapping = {
            "temple": (Temple, "templedetailsview"),
            "goshala": (Goshala, "getbygoshala"),
            "village": (Village, "villages"),
            "tourism": (TempleNearbyTourismPlace, "tourism-places"),
            "event": (Event, "detailviewevent"),
        }
        return mapping.get(content_type.lower())
    def clean_image_path(self, path):
        """
        Cleans unwanted characters from the image path.
        Removes quotes, brackets, and escaped slashes.
        """
        if not path:
            return None
        # Remove outer quotes and brackets if present
        cleaned = str(path).strip()
        cleaned = re.sub(r'^["\'\[\]]+|["\'\[\]]+$', '', cleaned)
        return cleaned
    def get(self, request, content_type, content_id):
        try:
            model_info = self.get_model_and_url(content_type)
            if not model_info:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid content type"
                }, status=400)
            ModelClass, url_path = model_info
            obj = ModelClass.objects.get(_id=content_id)
            share_url = f"https://gramadevata.com/{url_path}/{content_id}"
            image_url = None
            image_data = getattr(obj, 'image_location', None)
            if image_data:
                try:
                    if isinstance(image_data, str):
                        try:
                            image_paths = json.loads(image_data)
                            if isinstance(image_paths, list) and image_paths:
                                raw_path = image_paths[0]
                            else:
                                raw_path = image_data
                        except json.JSONDecodeError:
                            raw_path = image_data
                    elif isinstance(image_data, list) and image_data:
                        raw_path = image_data[0]
                    else:
                        raw_path = None
                    if raw_path:
                        cleaned_path = self.clean_image_path(raw_path)
                        image_url = f"https://sathayushstorage.blob.core.windows.net/sathayush/{cleaned_path}"
                except Exception as e:
                    print(f"Image processing error: {e}")
                    image_url = None
            share_message = {
                "_id": getattr(obj, '_id', 'No _id'),
                "name": getattr(obj, 'name', 'No name'),
                "desc": getattr(obj, 'desc', 'No desc'),
                "image": image_url,
                "share_url": share_url,
            }
            return JsonResponse({"status": "success", "data": share_message}, status=200)
        except ModelClass.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": f"{content_type.title()} not found"
            }, status=404)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
        



from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from ..models import Temple
import json


class ShareTemplePageView(APIView):

    def get_first_image(self, image_field):
        """Fix and extract first image from JSON, list or comma string."""
        if not image_field:
            return ""

        try:
            # JSON list
            if image_field.startswith("["):
                image_list = json.loads(image_field)
                if isinstance(image_list, list) and image_list:
                    return image_list[0]

            # comma separated
            if "," in image_field:
                return image_field.split(",")[0]

            # raw
            return image_field

        except:
            return image_field

    def get(self, request, id):
        temple = get_object_or_404(Temple, _id=id)

        # extract image
        image = self.get_first_image(temple.image or "")

        context = {
            "title": temple.name,
            "description": (temple.desc[:250] + "...") if temple.desc else "",
            "image": image,
            "url": temple.share_url or f"https://gramadevata.com/templedetailsview/{id}"
        }

        return render(request, "share/share_temple.html", context)
