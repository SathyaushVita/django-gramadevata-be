# from ..serializers import RegisterSerializer,LoginSerializer,RegisterSerializer1,VerifySerializer,ResendOtpSerializer,ResetSerializer,UserSerializer
from ..serializers import MoreDetailsSerializer,ResendOtpSerializer,VerifySerializer,LoginSerializer,FamilyImageSerializer,profileserializer,profileserializer1,profilegetSerializer
from rest_framework import viewsets,generics
from ..models import Register
from rest_framework .views import APIView,status
from rest_framework .response import Response
from ..enums import UserStatus
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from ..utils import generate_otp, validate_email,send_email,send_sms,Resend_sms,image_path_to_binary,save_image_to_azure,save_video_to_azure
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from django.shortcuts import get_object_or_404
import base64
from ..utils import save_image_to_folder
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
from django.db.models import Q
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils import send_welcome_email
from ..models import Register
from ..utils import (
    generate_otp,
    validate_email,
    send_email,
    send_sms,
    run_async
)

class Registerview(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if not username:
            return Response(
                {"error": "username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = "0000" if username in [
            "sathayushtechsolutions@gmail.com",
            "7680822565"
        ] else generate_otp()

        user = Register.objects.filter(
            Q(email=username) | Q(contact_number=username)
        ).first()

        if user:
            user.verification_otp = otp
            user.verification_otp_created_time = timezone.now()
            user.save()
            message = "OTP sent successfully"
        else:
            user = Register.objects.create(
                username=username,
                verification_otp=otp,
                verification_otp_created_time=timezone.now(),
                email=username if validate_email(username) else None,
                contact_number=username if not validate_email(username) else None
            )
            message = "OTP sent successfully"

        # ✅ ASYNC OTP SEND
        if validate_email(username):
            run_async(send_email, username, otp)
        else:
            run_async(send_sms, username, otp)

        return Response(
            {"message": message},
            status=status.HTTP_200_OK
        )
    


        



def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class LoginView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        verification_otp = request.data.get("verification_otp")

        user = None
        if validate_email(username):
            user = Register.objects.filter(
                email=username,
                verification_otp=verification_otp
            ).first() or Register.objects.filter(
                contact_number=username,
                verification_otp=verification_otp
            ).first()
        else:
            user = Register.objects.filter(
                contact_number=username,
                verification_otp=verification_otp
            ).first() or Register.objects.filter(
                email=username,
                verification_otp=verification_otp
            ).first()

        if not user:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if username in ["sathayushtechsolutions@gmail.com", "7680822565"] and verification_otp != "0000":
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ GET PUBLIC IP
        ip_address = get_client_ip(request)

        # 👇 Track activation
        was_inactive = user.status != "ACTIVE"

        user.status = "ACTIVE"
        user.ip_address = ip_address   # ✅ SAVE PUBLIC IP
        user.last_login = timezone.now()
        user.save()

        if was_inactive:
            send_welcome_email(user.email)

        profile_pic_link = None
        if user.profile_pic:
            profile_pic_link = image_path_to_binary(user.profile_pic)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.get_username(),
            "user_id": user.id,
            "is_member": user.is_member,
            "type": user.type,
            "profile_pic": profile_pic_link,
            "full_name": user.full_name,
            "ip_address": ip_address   # ✅ RETURN IP
        }, status=status.HTTP_200_OK)


# class LoginView(generics.GenericAPIView):
#     serializer_class = VerifySerializer
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         verification_otp = request.data.get('verification_otp')
#         # Check if user exists by either email or contact number
#         user = None
#         if validate_email(username):
#             user = Register.objects.filter(email=username, verification_otp=verification_otp).first() or Register.objects.filter(contact_number=username, verification_otp=verification_otp).first()
#         else:
#             user = Register.objects.filter(contact_number=username, verification_otp=verification_otp).first() or Register.objects.filter(email=username, verification_otp=verification_otp).first()
#         if user:
#             # Special case for specific email or contact number
#             if username in ["sathayushtechsolutions@gmail.com", "7680822565"] and verification_otp != "0000":
#                 return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
#             # Check OTP expiration
#             if user.verification_otp_created_time < timezone.now() - timezone.timedelta(hours=24):
#                 return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
#             # Update user status to ACTIVE
#             user.status = 'ACTIVE'
#             profile_pic_link = None
#             if user.profile_pic:
#                 profile_pic_link = image_path_to_binary(user.profile_pic)
#             user.save()
#             # Generate tokens


#             refresh = RefreshToken.for_user(user)
#             access = refresh.access_token

#             access['user_id'] = user.id
#             access['username'] = user.username
#             access['email'] = user.email
#             access['contact_number'] = user.contact_number
#             access['source'] = 'gramadevata'

#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(access),
#                 "sso_token": str(access),  # 🔥 IMPORTANT
#                 'username': user.get_username(),
#                 'user_id': user.id,
#                 "is_member": user.is_member,
#                 "type": user.type,
#                 "profile_pic": profile_pic_link,
#                 "full_name": user.full_name
#             }, status=status.HTTP_200_OK)


        




# class updateprofile(generics.GenericAPIView):
#     serializer_class = profileserializer

#     def put(self, request, id):
#         instance = get_object_or_404(Register, id=id)

#         # Get data from the request
#         profile_pic = request.data.get('profile_pic')
#         family_images = request.data.get('family_images', [])
#         pujari_certificates = request.data.get('pujari_certificate', [])
#         pujari_id_image = request.data.get('pujari_id_image')
#         pujari_video = request.data.get('pujari_video', [])

#         # 7 additional image fields
#         image_fields = [
#             'mf_image', 'f_mf_image', 'm_mf_image',
#             'ff_mf_image', 'fm_mf_image', 'mf_mf_image', 'mm_mf_image'
#         ]
#         image_field_data = {field: request.data.get(field, []) for field in image_fields}

#         # Normalize list-type fields
#         if not isinstance(family_images, list):
#             family_images = [family_images]
#         if not isinstance(pujari_certificates, list):
#             pujari_certificates = [pujari_certificates]
#         if not isinstance(pujari_video, list):
#             pujari_video = [pujari_video]
#         for field in image_fields:
#             if not isinstance(image_field_data[field], list):
#                 image_field_data[field] = [image_field_data[field]]

#         # Prepare serializer data with current values
#         mutable_data = request.data.copy()
#         mutable_data['profile_pic'] = instance.profile_pic
#         mutable_data['family_images'] = instance.family_images
#         mutable_data['pujari_certificate'] = instance.pujari_certificate
#         mutable_data['pujari_id_image'] = instance.pujari_id_image
#         mutable_data['pujari_video'] = instance.pujari_video
#         for field in image_fields:
#             mutable_data[field] = getattr(instance, field)
#         mutable_data['is_member'] = "true"

#         # Validate and save basic data
#         serializer = self.get_serializer(instance, data=mutable_data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(is_member='true')

#         # Save profile pic
#         if profile_pic and profile_pic != "null":
#             saved_location = save_image_to_azure(profile_pic, instance.id, instance.full_name, 'profile_pic')
#             if saved_location:
#                 instance.profile_pic = saved_location
#                 instance.save(update_fields=['profile_pic'])

#         # Save family images (append)
#         saved_family_images = instance.family_images or []
#         for image in family_images:
#             if image and image != "null":
#                 saved = save_image_to_azure(image, instance.id, instance.full_name, 'family_images')
#                 if saved:
#                     saved_family_images.append(saved)
#         if saved_family_images != instance.family_images:
#             instance.family_images = saved_family_images
#             instance.save(update_fields=['family_images'])

#         # Save pujari certificates (append)
#         pujari_certificates_db = instance.pujari_certificate or []
#         if isinstance(pujari_certificates_db, str):
#             try:
#                 pujari_certificates_db = json.loads(pujari_certificates_db)
#             except:
#                 pujari_certificates_db = []

#         for image in pujari_certificates:
#             if image and image != "null":
#                 saved = save_image_to_azure(image, instance.id, instance.full_name, 'pujari_certificate')
#                 if saved:
#                     pujari_certificates_db.append(saved)

#         instance.pujari_certificate = pujari_certificates_db
#         instance.save(update_fields=['pujari_certificate'])

#         # Save 7 special image fields (replace with max 2)
#         for field in image_fields:
#             images = image_field_data[field][:2]  # only first 2 images
#             new_images = []
#             for image in images:
#                 if image and image != "null":
#                     saved = save_image_to_azure(image, instance.id, instance.full_name, field)
#                     if saved:
#                         new_images.append(saved)
#             if new_images:
#                 setattr(instance, field, new_images)
#                 instance.save(update_fields=[field])

#         # Save pujari_id_image
#         if pujari_id_image and pujari_id_image != "null":
#             saved = save_image_to_azure(pujari_id_image, instance.id, instance.full_name, 'pujari_id_image')
#             if saved:
#                 instance.pujari_id_image = saved
#                 instance.save(update_fields=['pujari_id_image'])

# # ✅ Save multiple pujari videos (append)
#         pujari_video_db = instance.pujari_video or []
#         if isinstance(pujari_video_db, str):
#             try:
#                 pujari_video_db = json.loads(pujari_video_db)
#             except:
#                 pujari_video_db = []

#         for image in pujari_video:  # <- corrected variable name here
#             if image and image != "null":
#                 saved = save_video_to_azure(image, instance.id, instance.full_name, 'pujari_video')
#                 if saved:
#                     pujari_video_db.append(saved)

#         instance.pujari_video = pujari_video_db
#         instance.save(update_fields=['pujari_video'])



#         return Response(profileserializer(instance).data, status=status.HTTP_200_OK)

from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
import json

class updateprofile(generics.GenericAPIView):
    serializer_class = profileserializer

    @transaction.atomic
    def put(self, request, id):
        instance = get_object_or_404(Register, id=id)

        # -----------------------------
        # Get Data From Request
        # -----------------------------
        profile_pic = request.data.get('profile_pic')
        family_images = request.data.get('family_images', [])
        pujari_certificates = request.data.get('pujari_certificate', [])
        pujari_id_image = request.data.get('pujari_id_image')
        pujari_video = request.data.get('pujari_video', [])

        image_fields = [
            'mf_image', 'f_mf_image', 'm_mf_image',
            'ff_mf_image', 'fm_mf_image', 'mf_mf_image', 'mm_mf_image'
        ]
        image_field_data = {field: request.data.get(field, []) for field in image_fields}

        # -----------------------------
        # Normalize List Fields
        # -----------------------------
        if not isinstance(family_images, list):
            family_images = [family_images]

        if not isinstance(pujari_certificates, list):
            pujari_certificates = [pujari_certificates]

        if not isinstance(pujari_video, list):
            pujari_video = [pujari_video]

        for field in image_fields:
            if not isinstance(image_field_data[field], list):
                image_field_data[field] = [image_field_data[field]]

        # -----------------------------
        # ✅ Email & Contact Validation
        # -----------------------------
        mutable_data = request.data.copy()

        new_email = mutable_data.get('email', instance.email)
        new_contact_number = mutable_data.get('contact_number', instance.contact_number)

        if new_email and new_email != instance.email:
            if Register.objects.filter(email=new_email).exclude(id=instance.id).exists():
                return Response(
                    {"error": "This email is already registered with another account."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if new_contact_number and new_contact_number != instance.contact_number:
            if Register.objects.filter(contact_number=new_contact_number).exclude(id=instance.id).exists():
                return Response(
                    {"error": "This contact number is already registered with another account."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # -----------------------------
        # Preserve Existing File Fields
        # -----------------------------
        mutable_data['profile_pic'] = instance.profile_pic
        mutable_data['family_images'] = instance.family_images
        mutable_data['pujari_certificate'] = instance.pujari_certificate
        mutable_data['pujari_id_image'] = instance.pujari_id_image
        mutable_data['pujari_video'] = instance.pujari_video

        for field in image_fields:
            mutable_data[field] = getattr(instance, field)

        mutable_data['is_member'] = "true"

        # -----------------------------
        # Save Basic Fields
        # -----------------------------
        serializer = self.get_serializer(instance, data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_member='true')

        # -----------------------------
        # Save Profile Pic (Replace)
        # -----------------------------
        if profile_pic and profile_pic != "null":
            saved = save_image_to_azure(profile_pic, instance.id, instance.full_name, 'profile_pic')
            if saved:
                instance.profile_pic = saved

        # -----------------------------
        # Save Family Images (Append)
        # -----------------------------
        saved_family_images = instance.family_images or []

        for image in family_images:
            if image and image != "null":
                saved = save_image_to_azure(image, instance.id, instance.full_name, 'family_images')
                if saved:
                    saved_family_images.append(saved)

        instance.family_images = saved_family_images

        # -----------------------------
        # Save Pujari Certificates (Append)
        # -----------------------------
        pujari_certificates_db = instance.pujari_certificate or []

        if isinstance(pujari_certificates_db, str):
            try:
                pujari_certificates_db = json.loads(pujari_certificates_db)
            except:
                pujari_certificates_db = []

        for image in pujari_certificates:
            if image and image != "null":
                saved = save_image_to_azure(image, instance.id, instance.full_name, 'pujari_certificate')
                if saved:
                    pujari_certificates_db.append(saved)

        instance.pujari_certificate = pujari_certificates_db

        # -----------------------------
        # Save 7 Special Image Fields (Replace Max 2)
        # -----------------------------
        for field in image_fields:
            images = image_field_data[field][:2]
            new_images = []

            for image in images:
                if image and image != "null":
                    saved = save_image_to_azure(image, instance.id, instance.full_name, field)
                    if saved:
                        new_images.append(saved)

            if new_images:
                setattr(instance, field, new_images)

        # -----------------------------
        # Save Pujari ID Image (Replace)
        # -----------------------------
        if pujari_id_image and pujari_id_image != "null":
            saved = save_image_to_azure(pujari_id_image, instance.id, instance.full_name, 'pujari_id_image')
            if saved:
                instance.pujari_id_image = saved

        # -----------------------------
        # Save Pujari Videos (Append)
        # -----------------------------
        pujari_video_db = instance.pujari_video or []

        if isinstance(pujari_video_db, str):
            try:
                pujari_video_db = json.loads(pujari_video_db)
            except:
                pujari_video_db = []

        for video in pujari_video:
            if video and video != "null":
                saved = save_video_to_azure(video, instance.id, instance.full_name, 'pujari_video')
                if saved:
                    pujari_video_db.append(saved)

        instance.pujari_video = pujari_video_db

        # -----------------------------
        # Final Save (Single DB Hit)
        # -----------------------------
        instance.save()

        return Response(
            profileserializer(instance).data,
            status=status.HTTP_200_OK
        )



class GetProfileById(generics.GenericAPIView):
    serializer_class = MoreDetailsSerializer
    # permission_classes = [IsAuthenticated]  # Ensure user is authenticated to access profile

    def get(self, request, id):
        instance = get_object_or_404(Register, id=id)
        
        # Convert family_images to base64
        if instance.family_images:
            family_images_base64 = []
            for image_path in instance.family_images:
                base64_image = image_path_to_binary(image_path)
                if base64_image:
                    family_images_base64.append(base64_image)
            instance.family_images = family_images_base64

        # Check if the requesting user is the owner of the profile
        if request.user == instance:
            # User is viewing their own profile, show all data
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If account type is PRIVATE and the user is not the owner, limit the fields
        if instance.account_type == 'PRIVATE':
            # Only include specific fields for PRIVATE account type
            allowed_fields = ["full_name", "profile_pic", "is_member", "account_type", "type", "id"]
            serializer = self.get_serializer(instance)
            data = {field: serializer.data[field] for field in allowed_fields}
            return Response(data, status=status.HTTP_200_OK)

        # For PUBLIC, return all fields
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)





class ProfileUpdate(generics.GenericAPIView):
    serializer_class = FamilyImageSerializer
    def put(self, request, id):
        instance = get_object_or_404(Register, id=id)
        profile_pic = request.data.get('profile_pic')
        family_images = request.data.get('family_images', [])
        # Ensure family_images is a list
        if not isinstance(family_images, list):
            family_images = [family_images]
        # Check the total number of family images after adding new ones
        existing_family_images = instance.family_images or []
        total_family_images = len(existing_family_images) + len(family_images)
        if total_family_images > 10:
            return Response(
                {"error": "You can upload a maximum of 10 family images."},
                status=status.HTTP_400_BAD_REQUEST
            )
        mutable_data = request.data.copy()
        mutable_data['profile_pic'] = instance.profile_pic  # Preserve existing profile_pic
        mutable_data['family_images'] = existing_family_images  # Preserve existing family images
        serializer = self.get_serializer(instance, data=mutable_data, partial=True)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['is_member'] = "YES"
        serializer.save()
        # Save the profile picture if provided
        if profile_pic and profile_pic != "null":
            saved_location = save_image_to_azure(
                profile_pic,
                instance.id,
                instance.full_name,
                'profile_pic'
            )
            if saved_location:
                instance.profile_pic = saved_location
                instance.save(update_fields=['profile_pic'])
        # Save and append new family images if provided
        saved_family_image_paths = existing_family_images.copy()
        for image_data in family_images:
            if image_data and image_data != "null":
                saved_location = save_image_to_azure(
                    image_data,
                    instance.id,
                    instance.full_name,
                    'family_images'
                )
                if saved_location:
                    saved_family_image_paths.append(saved_location)
        # Update family_images field if new images were added
        if saved_family_image_paths != existing_family_images:
            instance.family_images = saved_family_image_paths
            instance.save(update_fields=['family_images'])
        return Response(
            FamilyImageSerializer(instance).data,
            status=status.HTTP_200_OK
        )











    
class updateRoots(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = profileserializer1
    def put(self, request, id):
        # Get the instance of the user profile to update
        instance = get_object_or_404(Register, id=id)
       
        serializer = profileserializer1(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
       
        serializer.save()
       
       

        return Response({"message": "Updated Successfully"}, status=status.HTTP_200_OK)



class DeleteImage(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = FamilyImageSerializer
    def post(self, request, id):
        action = request.data.get('action')
        if action == 'delete_family_image':
            return self.delete_family_image(request, id)
        return Response(
            {"error": "Invalid action."},
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete_family_image(self, request, id):
        instance = get_object_or_404(Register, id=id)
        # Get index from request data
        try:
            index = int(request.data.get('index'))
        except (TypeError, ValueError):
            return Response(
                {"error": "A valid index is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Validate index range
        if index < 0 or index >= len(instance.family_images):
            return Response(
                {"error": "Index out of range."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Retrieve the file path to delete
        file_path_to_delete = instance.family_images[index]
        # Full file path to delete
        file_full_path = os.path.join(settings.FILE_URL, file_path_to_delete)
        if os.path.exists(file_full_path):
            os.remove(file_full_path)
        # Remove the path from the database
        instance.family_images.pop(index)
        instance.save(update_fields=['family_images'])
        return Response(
            {"message": "Family image deleted successfully."},
            status=status.HTTP_200_OK
        )
# To perform above code use this code in swaggers
# {
#     "action": "delete_family_image",
#     "index": 4
# }




# class GetProfile(APIView):
#     def get(self, request):
#         queryset = Register.objects.all()
#         serializer = profileget(queryset, many=True)
#         response_data = serializer.data

#         for item in response_data:
#             profile_pic_path = item.get('profile_pic')
#             if profile_pic_path:
#                 try:
#                     with open(profile_pic_path, 'rb') as image_file:
#                         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#                     item['profile_pic'] = encoded_string
#                 except FileNotFoundError:
#                     item['profile_pic'] = None
#         return Response(response_data, status=status.HTTP_200_OK)
    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Register
from ..enums.gender_enum import Gender
from ..enums import MemberStatus

# class GetProfile(APIView):
#     def get(self, request):
#         try:
#             search_query = request.query_params.get('search', None)

#             # Base queryset – recent first
#             queryset = Register.objects.all().order_by('-date_joined')

#             # Apply search
#             if search_query:
#                 queryset = queryset.filter(
#                     Q(username__icontains=search_query) |
#                     Q(full_name__icontains=search_query)
#                 )

#             serializer = profilegetSerializer(queryset, many=True)

#             # Counts
#             total_users = queryset.count()
#             members_count = queryset.filter(is_member=MemberStatus.true.value).count()
#             non_members_count = queryset.filter(is_member=MemberStatus.false.value).count()
#             male_count = queryset.filter(gender=Gender.MALE.value).count()
#             female_count = queryset.filter(gender=Gender.FEMALE.value).count()

#             data = {
#                 "user_count": {
#                     "total": total_users,
#                     "members": members_count,
#                     "non_members": non_members_count,
#                     "male": male_count,
#                     "female": female_count
#                 },
#                 "profiles": serializer.data
#             }

#             return Response(data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class GetProfile(APIView):

    def get(self, request):
        try:
            search_query = request.query_params.get('search')
            activity = request.query_params.get('activity')  # ACTIVE / INACTIVE

            active_time = timezone.now() - timedelta(minutes=5)

            # 🔹 Base queryset (Recent users first by date_joined)
            queryset = Register.objects.all().order_by('-date_joined')

            # 🔍 Search filter
            if search_query:
                queryset = queryset.filter(
                    Q(username__icontains=search_query) |
                    Q(full_name__icontains=search_query)
                )

            # 🟢 Activity filter (ONLY for profiles list)
            if activity == "ACTIVE":
                queryset = queryset.filter(last_seen__gte=active_time)
            elif activity == "INACTIVE":
                queryset = queryset.exclude(last_seen__gte=active_time)

            serializer = profilegetSerializer(queryset, many=True)

            # 📊 GLOBAL COUNTS
            total_users = Register.objects.count()

            members_count = Register.objects.filter(
                is_member=MemberStatus.true.value
            ).count()

            non_members_count = Register.objects.filter(
                is_member=MemberStatus.false.value
            ).count()

            male_count = Register.objects.filter(
                gender=Gender.MALE.value
            ).count()

            female_count = Register.objects.filter(
                gender=Gender.FEMALE.value
            ).count()

            active_users = Register.objects.filter(
                last_seen__gte=active_time
            ).count()

            inactive_users = total_users - active_users

            data = {
                "user_count": {
                    "total": total_users,
                    "members": members_count,
                    "non_members": non_members_count,
                    "male": male_count,
                    "female": female_count,
                    "active": active_users,
                    "inactive": inactive_users
                },
                "profiles": serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = request.user  # Get the logged-in user

        # Print debug statement
        print(f"Logged-in User ID: {user.id}, Requested User ID: {id}")

        # Ensure the logged-in user can delete only their own profile
        if str(user.id) != str(id):
            print("Unauthorized deletion attempt detected.")  # Debugging print
            return Response(
                {"detail": "You are not allowed to delete another user's profile.", "code": "forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the user object and delete
        profile = get_object_or_404(Register, id=id)
        profile.delete()

        return Response({"detail": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    




from ..enums import MemberStatus

from ..models import ConnectModel, CommentModel, ChatModel
from django.db import connection
from django.db.models import Q
import json
def log_deleted_user_data(profile, role: str, deleted_by):
    # Step 1: Basic profile data
    if role == "member":
        profile_data = {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "father_name": profile.father_name,
            "contact_number": profile.contact_number,
            "email": profile.email,
            "gender": profile.gender,
            "account_type": profile.account_type,
            "type": profile.type,
            "marital_status": getattr(profile, "marital_status", None),
            "surname": getattr(profile, "surname", None),
            "mother_name": getattr(profile, "mother_name", None),
            "gotram": getattr(profile, "gotram", None),
            "siblings": getattr(profile, "siblings", None),
            "husband": getattr(profile, "husband", None),
            "wife": getattr(profile, "wife", None),
            "children": getattr(profile, "children", None),
            "profile_pic": getattr(profile, "profile_pic", None),
        }
    elif role == "pujari":
        profile_data = {
            "voluntary_level": getattr(profile, "voluntary_level", None),
            "pujari_expertise": getattr(profile, "pujari_expertise", None),
            "pujari_id_type": getattr(profile, "pujari_id_type", None),
            "pujari_id_image": getattr(profile, "pujari_id_image", None),
            "pujari_certificate_type": getattr(profile, "pujari_certificate_type", None),
            "issued_by": getattr(profile, "issued_by", None),
            "pujari_type": getattr(profile, "pujari_type", None),
            "pujari_video": getattr(profile, "pujari_video", []),
            "pujari_certificate": getattr(profile, "pujari_certificate", None),
            "working_temple": getattr(profile, "working_temple", None),
            "pujari_designation": getattr(profile, "pujari_designation", None),
        }
    else:
        profile_data = {}
    # Step 2: Fetch related data
    connections_data = list(ConnectModel.objects.filter(user=profile).values())
    comments_data = list(CommentModel.objects.filter(user=profile).values())
    chats_data = list(ChatModel.objects.filter(user=profile).values())  # :white_check_mark: fixed
    # Step 3: Prepare final payload
    full_data = {
        "profile": profile_data,
        "connections": connections_data,
        "comments": comments_data,
        "chats": chats_data,
    }
    # Step 4: Save into deleted_user_data table
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO deleted_user_data (user_id, deleted_by, role, data)
            VALUES (%s, %s, %s, %s)
        """, [
            str(profile.id), str(deleted_by.id), role, json.dumps(full_data, default=str)
        ])
    # Step 5: Now delete the data
    connections_data = list(ConnectModel.objects.filter(user_id=profile.id).values())
    comments_data = list(CommentModel.objects.filter(user_id=profile.id).values())
    chats_data = list(ChatModel.objects.filter(user_id=profile.id).values())
  # :white_check_mark: fixed
def update_member_type_on_delete(current_type, remove_role):
    if not current_type:
        return ""
    roles = current_type.upper().split("/")
    remove_role = remove_role.upper()
    if remove_role in roles:
        roles.remove(remove_role)
    return "/".join(roles)



class DeleteMemberView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        user = request.user
        if str(user.id) != str(id):
            return Response(
                {"detail": "You are not allowed to delete another user's member data."},
                status=status.HTTP_403_FORBIDDEN
            )
        profile = get_object_or_404(Register, id=id)
        if "PUJARI" in (profile.type or "").upper():
            return Response(
                {"detail": "Please delete your Pujari details before deleting Member details."},
                status=status.HTTP_400_BAD_REQUEST
            )
        log_deleted_user_data(profile, "member", request.user)
        # Clear member-related fields
        profile.full_name = None
        profile.first_name = None
        profile.last_name = None
        profile.father_name = None
        # profile.contact_number = None
        profile.gender = None
        profile.account_type = None
        # profile.email = None
        profile.marital_status = None
        profile.surname = None
        profile.mother_name = None
        profile.gotram = None
        profile.siblings = None
        profile.husband = None
        profile.wife = None
        profile.children = None
        profile.profile_pic=None
        ConnectModel.objects.filter(user=profile).delete()
        CommentModel.objects.filter(user=profile).delete()
        ChatModel.objects.filter(user=profile).delete()
        # Update member status and type
        profile.is_member = MemberStatus.false.value
        profile.type = update_member_type_on_delete(profile.type, "member")
        profile.save()
        return Response(
            {"detail": "Member details removed successfully."},
            status=status.HTTP_200_OK
        )
    



class DeletePujariView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        user = request.user
        if str(user.id) != str(id):
            return Response(
                {"detail": "You are not allowed to delete another user's pujari data."},
                status=status.HTTP_403_FORBIDDEN
            )
        profile = get_object_or_404(Register, id=id)
        log_deleted_user_data(profile, "pujari", request.user)
        # Clear pujari-related fields
        profile.voluntary_level = None
        profile.pujari_expertise = None
        profile.pujari_id_type = None
        profile.pujari_id_image = None
        profile.pujari_certificate_type = None
        profile.issued_by = None
        profile.pujari_type = None
        profile.pujari_video = []
        profile.pujari_certificate = None
        profile.working_temple = None
        profile.pujari_designation = None
        # Clear M2M fields
        profile.pujari_category.clear()
        profile.pujari_sub_category.clear()
        ConnectModel.objects.filter(user=profile).delete()
        CommentModel.objects.filter(user=profile).delete()
        ChatModel.objects.filter(user=profile).delete()
        # Update type safely
        new_type = update_member_type_on_delete(profile.type, "pujari")
        if new_type:
            profile.type = new_type
        else:
            if profile.is_member == MemberStatus.true.value:
                profile.type = "MEMBER"
            else:
                profile.type = ""
        profile.save()
        return Response(
            {"detail": "Pujari details removed successfully."},
            status=status.HTTP_200_OK
        )








from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class AdminProfileById(generics.GenericAPIView):
    serializer_class = MoreDetailsSerializer

    def get(self, request, id):
        instance = get_object_or_404(Register, id=id)

        # Convert family_images to base64
        if instance.family_images:
            family_images_base64 = []
            for image_path in instance.family_images:
                base64_image = image_path_to_binary(image_path)
                if base64_image:
                    family_images_base64.append(base64_image)
            instance.family_images = family_images_base64

        # Always return full profile (no PRIVATE / PUBLIC check)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)



#usersstatus and active and inactive and last-seen

class UsersStatusView(APIView):

    def get(self, request):
        ACTIVE_THRESHOLD_MINUTES = 5
        now = timezone.now()
        active_since = now - timedelta(minutes=ACTIVE_THRESHOLD_MINUTES)

        active_qs = Register.objects.filter(last_seen__gte=active_since)
        inactive_qs = Register.objects.filter(
            Q(last_seen__lt=active_since) | Q(last_seen__isnull=True)
        )

        def build_users(qs):
            users = []
            for u in qs:
                pic = image_path_to_binary(u.profile_pic) if u.profile_pic else None
                users.append({
                    "id": u.id,
                    "full_name": u.full_name,
                    "contact_number": u.contact_number,
                    "email": u.email,
                    "last_seen": u.last_seen,
                    "profile_pic": pic
                })
            return users

        active_users = build_users(active_qs)
        inactive_users = build_users(inactive_qs)

        return Response({
            "active_users_count": len(active_users),
            "inactive_users_count": len(inactive_users),
            "active_users": active_users,
            "inactive_users": inactive_users
        })