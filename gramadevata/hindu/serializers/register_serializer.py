from rest_framework import serializers
from ..models import Register
from .comment_serializer import CommentSerializer
from .connect_serializer import ConnectModelSerializer1
from .member_serializer import MemberSerializer1
from .temple_serializers import TempleSerializer1
from ..utils import image_path_to_binary,video_path_to_binary
from ..serializers.event_serializer import EventSerializer1
from ..serializers.goshala_serializer import GoshalaSerializer1
from ..models import Temple
from .favorite_temples_serializers import FavoriteTempleSerializer
from django.conf import settings
from .visit_temple_serializer import VisitTempleSerializer
from .pujari_category_serializer import PujariCategeorySerializer
from .pujari_subcategory_serializer import PujariSubCategorySerializer
from ..models import PujariCategory,PujariSubCategory
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    # full_name = serializers.CharField(max_length=255)
    class Meta:
        model = Register
        fields =["username"]
        # exclude = [
        #     'verification_otp', 'verification_otp_created_time',
        #     'verification_otp_resend_count'
        # ]

        
class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username","verification_otp"]


class ResendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields =["username"]


class TempleSerializerForProfile(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    class Meta:
        model = Temple
        fields = ['_id', 'name', 'image_location','status']

    def get_image_location(self, instance):
        filename = instance.image_location
        
        # Check if filename is a list or a string
        if isinstance(filename, list):
            # If it's already a list, return it as is
            image_paths = filename
        elif isinstance(filename, str):
            # If it's a string, attempt to parse it as a list-like string
            image_paths = filename.strip('[]').replace('"', '').split(',')
            image_paths = [path.strip() for path in image_paths]  # Clean up any extra spaces
        else:
            # If it's neither a list nor a string, return an empty list
            image_paths = []

        # Apply binary conversion (assuming `image_path_to_binary` is defined)
        return [image_path_to_binary(path) for path in image_paths]



class MoreDetailsSerializer(serializers.ModelSerializer):
    pujari_category_detail = PujariCategeorySerializer(many=True, read_only=True, source="pujari_category")
    pujari_sub_category_detail = PujariSubCategorySerializer(many=True, read_only=True, source="pujari_sub_category")
    Connections = ConnectModelSerializer1(many=True, read_only=True)
    temples = TempleSerializerForProfile(many=True, read_only=True)
    temples_count = serializers.SerializerMethodField()
    goshalas = GoshalaSerializer1(many=True, read_only=True)
    events = EventSerializer1(many=True, read_only=True)
    profile_pic = serializers.SerializerMethodField()
    pujari_certificate = serializers.SerializerMethodField()
    pujari_id_image = serializers.SerializerMethodField()
    pujari_video = serializers.SerializerMethodField()  # Added this line
    favorite = FavoriteTempleSerializer(many=True, read_only=True)
    visit_temples = VisitTempleSerializer(many=True, read_only=True)
    mf_image = serializers.SerializerMethodField()
    f_mf_image = serializers.SerializerMethodField()
    m_mf_image = serializers.SerializerMethodField()
    ff_mf_image = serializers.SerializerMethodField()
    fm_mf_image = serializers.SerializerMethodField()
    mf_mf_image = serializers.SerializerMethodField()
    mm_mf_image = serializers.SerializerMethodField()



    def convert_images_list(self, images_list):
        if not images_list:
            return []
        if not isinstance(images_list, list):
            images_list = [images_list]
        
        result = []
        for img in images_list:
            if img and img != "null":
                binary = image_path_to_binary(img)
                if binary:
                    result.append(binary)
        return result



    def get_mf_image(self, instance):
        return self.convert_images_list(instance.mf_image)

    def get_f_mf_image(self, instance):
        return self.convert_images_list(instance.f_mf_image)

    def get_m_mf_image(self, instance):
        return self.convert_images_list(instance.m_mf_image)

    def get_ff_mf_image(self, instance):
        return self.convert_images_list(instance.ff_mf_image)

    def get_fm_mf_image(self, instance):
        return self.convert_images_list(instance.fm_mf_image)

    def get_mf_mf_image(self, instance):
        return self.convert_images_list(instance.mf_mf_image)

    def get_mm_mf_image(self, instance):
        return self.convert_images_list(instance.mm_mf_image)


    def get_pujari_certificate(self, instance):
        # Same for certificate which is stored as list of images (JSONField)
        return self.convert_images_list(instance.pujari_certificate)

    def get_profile_pic(self, instance):
        filename = instance.profile_pic
        if filename:
            # Check if filename is a list and handle it
            if isinstance(filename, list):
                filename = filename[0]  # Choose the first item or handle the list as needed
            format = image_path_to_binary(filename)
            return format
        return ''

    # def get_pujari_certificate(self, instance):
    #     filename = instance.pujari_certificate
    #     if filename:
    #         # Check if filename is a list and handle it
    #         if isinstance(filename, list):
    #             filename = filename[0]  # Choose the first item or handle the list as needed
    #         format = image_path_to_binary(filename)
    #         return format
    #     return ''

    def get_pujari_id_image(self, instance):
        filename = instance.pujari_id_image
        if filename:
            # Check if filename is a list and handle it
            if isinstance(filename, list):
                filename = filename[0]  # Choose the first item or handle the list as needed
            format = image_path_to_binary(filename)
            return format
        return ''

    def get_pujari_video(self, instance):
        filenames = instance.pujari_video
        if not filenames:
            return []

        if not isinstance(filenames, list):
            filenames = [filenames]

        videos = []
        for filename in filenames:
            if filename and filename != "null":
                binary = video_path_to_binary(filename)
                if binary:
                    videos.append(binary)
        return videos
    


    def get_temples_count(self, obj):
        return obj.temples.count()


    class Meta:
        model = Register
        fields = [
            "temples_count", "id", "full_name", 'surname', "gotram", "father_name", "profile_pic", "contact_number",
            "gender", "dob", "type", "pujari_certificate", "working_temple",
            "is_member", "Connections", "temples", "goshalas", "events", "family_images", 'email', 'account_type',
            'mother_name', 'paternal_grandmother_name', 'paternal_grandfather_name',
            'paternal_great_grandfather_name', 'paternal_great_grandmother_name',
            'paternal_grandmother_father_name', 'paternal_grandmother_mother_name',
            'maternal_grandfather_name', 'maternal_grandmother_name',
            'maternal_great_grandfather_name', 'maternal_great_grandmother_name',
            'maternal_grandmother_father_name', 'maternal_grandmother_mother_name',
            'marital_status', 'wife', 'husband', 'children', 'siblings', "favorite", "voluntary_level", "pujari_expertise",
            "pujari_id_type", "pujari_certificate_type", "pujari_id_image", "pujari_category", "pujari_sub_category",
            "issued_by", "pujari_type", "pujari_video" ,"pujari_category_detail","pujari_sub_category_detail","pujari_designation","visit_temples",
            "mf_image","f_mf_image","m_mf_image","ff_mf_image","fm_mf_image","mf_mf_image","mm_mf_image","desc"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # # Handle image URLs
        # if instance.image_location:
        #     if isinstance(instance.image_location, str):
        #         image_locations = instance.image_location.strip('[]').replace('"', '').split(',')
        #         image_locations = [path.strip() for path in image_locations]
        #     elif isinstance(instance.image_location, list):
        #         image_locations = [path.strip() for path in instance.image_location if isinstance(path, str)]
        #     else:
        #         image_locations = []
        #     image_locations = [f"{settings.FILE_URL}{path}" for path in image_locations if path and path != "null"]
        #     representation['image_location'] = image_locations
        # else:
        #     representation['image_location'] = []

        # # Handle event video URLs
        if instance.pujari_video:
            if isinstance(instance.pujari_video, str):
                pujari_videos = instance.pujari_video.strip('[]').replace('"', '').split(',')
                pujari_videos = [path.strip() for path in pujari_videos]
            elif isinstance(instance.pujari_video, list):
                pujari_videos = [path.strip() for path in instance.pujari_video if isinstance(path, str)]
            else:
                pujari_videos = []
            pujari_videos = [f"{settings.FILE_URL}{path}" for path in pujari_videos if path and path != "null"]
            representation['pujari_video'] = pujari_videos
        else:
            representation['pujari_video'] = []

        return representation



class MoreDetailsSerializer1(serializers.ModelSerializer):
    profile_pic=serializers.SerializerMethodField()

    def get_profile_pic(self, instance):
        filename = instance.profile_pic
        if filename:
            format = image_path_to_binary(filename)
            return format
        return ''
    

    


    class Meta:
        model = Register
        fields = "__all__"
      
class FamilyImageSerializer(serializers.ModelSerializer):
    family_images = serializers.ListField(child=serializers.CharField(), required=False)
    class Meta:
        model = Register
        fields = ["family_images"]
    

# class profileserializer(serializers.ModelSerializer):
#     class Meta:
#         model=Register
#         fields=["id","full_name",'gender','account_type',"father_name","profile_pic","dob","contact_number","email",'mother_name','father_father_name','father_mother_name','grandfather_father_name_ff','grandfather_mother_name_ff','grandfather_father_name_fm','grandfather_mother_name_fm','mother_father_name','mother_mother_name','grandfather_father_name_mf','grandfather_mother_name_mf','grandmother_father_name_mm','grandmother_mother_name_mm']

# class profileserializer(serializers.ModelSerializer):


#     class Meta:
#         model=Register
#         fields=["id","full_name",'surname','gotram','gender','account_type',"father_name","profile_pic","dob",
#                 "contact_number","working_temple","pujari_certificate","pujari_designation","family_images","email",'mother_name', 'paternal_grandmother_name',
#                 'paternal_grandfather_name','paternal_great_grandfather_name','paternal_great_grandmother_name',
#                 'paternal_grandmother_father_name','paternal_grandmother_mother_name',
#                 'maternal_grandfather_name','maternal_grandmother_name',
#                 'maternal_great_grandfather_name','maternal_great_grandmother_name',
#                 'maternal_grandmother_father_name','maternal_grandmother_mother_name',
#                 'marital_status','wife','husband','children','siblings','voluntary_level',"pujari_expertise","pujari_id_type","pujari_certificate_type","pujari_id_image",
#                 "pujari_category","pujari_sub_category","issued_by","pujari_type","pujari_video"]
        


from .pujari_category_serializer import PujariCategeorySerializer
from .pujari_subcategory_serializer import PujariSubCategorySerializer
from ..models import PujariCategory,PujariSubCategory

class profileserializer(serializers.ModelSerializer):
    # ✅ For reading
    pujari_category_detail = PujariCategeorySerializer(many=True, read_only=True, source="pujari_category")
    pujari_sub_category_detail = PujariSubCategorySerializer(many=True, read_only=True, source="pujari_sub_category")

    # ✅ For writing
    pujari_category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PujariCategory.objects.all(), write_only=True
    )
    pujari_sub_category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PujariSubCategory.objects.all(), write_only=True
    )

    class Meta:
        model = Register
        fields = [
            "id", "full_name", 'surname', 'gotram', 'gender', 'account_type', "father_name", "profile_pic", "dob",
            "contact_number", "working_temple", "pujari_certificate", "pujari_designation", "family_images", "email",
            'mother_name', 'paternal_grandmother_name', 'paternal_grandfather_name', 'paternal_great_grandfather_name',
            'paternal_great_grandmother_name', 'paternal_grandmother_father_name', 'paternal_grandmother_mother_name',
            'maternal_grandfather_name', 'maternal_grandmother_name', 'maternal_great_grandfather_name',
            'maternal_great_grandmother_name', 'maternal_grandmother_father_name', 'maternal_grandmother_mother_name',
            'marital_status', 'wife', 'husband', 'children', 'siblings', 'voluntary_level', "pujari_expertise",
            "pujari_id_type", "pujari_certificate_type", "pujari_id_image",
            "pujari_category", "pujari_category_detail",
            "pujari_sub_category", "pujari_sub_category_detail",
            "issued_by", "pujari_type", "pujari_video","pujari_designation","mf_image","f_mf_image","m_mf_image","ff_mf_image",
            "fm_mf_image","mf_mf_image","mm_mf_image","desc"
        ]




class profileserializer1(serializers.ModelSerializer):
    class Meta:
        model=Register
        fields=["father_name","email",'mother_name', 'paternal_grandmother_name',
                'paternal_grandfather_name','paternal_great_grandfather_name','paternal_great_grandmother_name',
                'paternal_grandmother_father_name','paternal_grandmother_mother_name',
                'maternal_grandfather_name','maternal_grandmother_name',
                'maternal_great_grandfather_name','maternal_great_grandmother_name',
                'maternal_grandmother_father_name','maternal_grandmother_mother_name',
                'marital_status','wife','husband','children','siblings',"desc"]
        





# from rest_framework import serializers
# from ..models import Register
# from ..enums import MemberStatus
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Register
#         fields = '__all__'

#     def to_representation(self, instance):
#         data = super().to_representation(instance)

#         # Hide fields if user is not a member
#         if instance.is_member == MemberStatus.false.value:
#             for field in ['full_name', 'profile_pic', 'account_type', 'type', 'father_name','gender','email']:
#                 data.pop(field, None)

#         return data









from django.utils.timesince import timesince
from django.utils import timezone

from ..utils import get_user_activity_status


class profilegetSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()
    relative_time = serializers.SerializerMethodField()
    activity_status = serializers.SerializerMethodField()
    last_seen_time = serializers.SerializerMethodField()

    # Joined time (already working)
    def get_relative_time(self, instance):
        if not instance.date_joined:
            return None
        return f"{timesince(instance.date_joined)} ago"

    # ACTIVE / INACTIVE
    def get_activity_status(self, instance):
        return get_user_activity_status(instance)

    # Last seen like "3 minutes ago"
    def get_last_seen_time(self, instance):
        if not instance.last_seen:
            return None
        return f"{timesince(instance.last_seen)} ago"

    # Profile pic
    def get_profile_pic(self, instance):
        filename = instance.profile_pic
        if filename:
            if isinstance(filename, list):
                filename = filename[0]
            return image_path_to_binary(filename)
        return None

    class Meta:
        model = Register
        fields = [
            "id",
            "full_name",
            "surname",
            "gotram",
            "father_name",
            "profile_pic",
            "contact_number",
            "gender",
            "dob",
            "type",
            "is_member",
            "email",
            "desc",
            "relative_time",     
            "activity_status",   
            "last_seen_time"      
        ]
