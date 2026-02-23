from django.core.mail import send_mail
import random
from django.conf import settings
import re
import string
import requests
import base64
import os
from rest_framework.pagination import PageNumberPagination
import uuid
from io import BytesIO
from PIL import Image
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.core.files.base import ContentFile
# from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination



class CustomPagination(PageNumberPagination):
    page_size =50
    page_size_query_param = 'page_size'
    max_page_size = 90




def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip 

    


def send_email(emil,otp):
    subject = f'your GRAMADEVATA account verfication email is:'
    message = f'your otp is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,emil)
from django.core.mail import send_mail
import ssl
import certifi
from django.core.mail import get_connection, EmailMessage


# def send_email(to_email, otp):
#     subject = "Your OTP Code"
#     message = f"Your OTP is: {otp}"
#     ssl_context = ssl.create_default_context(cafile=certifi.where())
#     connection = get_connection(
#     host='emphasis.herosite.pro',
#     port=465,  # or 587 depending on TLS/SSL
#     username='info@gramadevata.com',
#     password='Vishnu@143$&',
#     use_tls=False,       # Set to True if using 587 with STARTTLS
#     use_ssl=True         # Set to True if using 465
# )
#     connection.ssl_context = ssl_context  # Apply the certifi context
#     email = EmailMessage(
#         subject,
#         message,
#         'info@gramadevata.com',
#         [to_email],
#         connection=connection
#     )
#     email.send()

def generate_otp(length = 4):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    if not re.match(email_regex, email):
        return False
    return True   
    



sms_user = settings.SMS_USER
sms_password = settings.SMS_PASSWORD
sms_sender = settings.SMS_SENDER
sms_type = settings.SMS_TYPE
sms_template_id = settings.SMS_TEMPLATE_ID
RESEND_SMS = settings.RESEND_SMS_TEMP


def send_sms(username, otp):
    
    
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}&message=Dear user your OTP to verify your Gramadevata User account is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={sms_template_id}"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP")


def Resend_sms(username, otp):
    
    # url = f"http://api.bulksmsgateway.in/sendmessage.php?user={sms_user}&password={sms_password}&mobile={username}message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender={sms_sender}&type={sms_type}&template_id={RESEND_SMS}"
    url = f"http://api.bulksmsgateway.in/sendmessage.php?user=Sathayushtech&password=Sathayushtech@1&mobile={username}&message=Dear user your OTP to reset your Gramadevata account Password is {otp}. Thank You! team Sathayush.&sender=STYUSH&type=3&template_id=1207170963828012432"

    print(url)  
    response = requests.get(url)
    print(response.text) 
    print("Sent Mobile OTP")




def image_path_to_binary(filename):
    img_url = settings.FILE_URL
    
    print(img_url,"ewrtyju")
    img_path = os.path.join(img_url, filename)  # Assuming settings.MEDIA_ROOT contains the directory where your images are stored
    print(img_path, "---------------------------------")

    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded_image = base64.b64encode(image_data)
            # print(base64_encoded_image)
            return img_path
    else:
        # print("File not found:", img_path)
        return img_path
    



# def save_image_to_folder(image_location, _id,name):
    
#     image_data = base64.b64decode(image_location)
    
    
#     folder_name = str(_id)
#     img_url = settings.FILE_URL
    
    
#     folder_path = os.path.join(img_url,"temple", folder_name)
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
    
   
#     image_name = name+".jpg"
#     image_path = os.path.join(folder_path, image_name)
#     with open(image_path, "wb") as image_file:
#         image_file.write(image_data)

#     return image_path



# def save_image_to_folder(image_location, _id, name, folder_type):
#     image_data = base64.b64decode(image_location)
#     folder_name = str(_id)
#     img_url = settings.FILE_URL
#     folder_path = os.path.join(img_url, "temple", folder_name, folder_type)
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     image_name = name + ".jpg"
#     image_path = os.path.join(folder_path, image_name)
#     with open(image_path, "wb") as image_file:
#         image_file.write(image_data)
#     return image_path


def save_image_to_folder(image_data, _id, name, entity_type):
    decoded_image = base64.b64decode(image_data)
    folder_name = str(_id)
    img_url = settings.FILE_URL
    folder_path = os.path.join(img_url, entity_type, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_name = f"{name}_{uuid.uuid4().hex[:8]}.jpg"
    image_path = os.path.join(folder_path, image_name)
    with open(image_path, "wb") as image_file:
        image_file.write(decoded_image)
    relative_image_path = os.path.join(entity_type, folder_name, image_name)
    return relative_image_path




def save_image_to_azure(image_data, _id, name, entity_type):
    # Decode base64 image
    decoded_image = base64.b64decode(image_data)
    
    # Create a folder name based on the provided _id and entity_type
    folder_name = str(_id)
    
    # Generate unique image name
    image_name = f"{name}_{uuid.uuid4().hex[:8]}.jpg"
    
    # Azure settings
    container_name = 'sathayush'
    folder_path = f"{entity_type}/{folder_name}/"  # Example: 'temple/1234/'
    blob_name = f"{folder_path}{image_name}"  # Full path for the image in Azure Blob Storage
    print(blob_name,"3efrgth")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the image to Azure Blob Storage
    blob_client.upload_blob(decoded_image, blob_type="BlockBlob", overwrite=True)

    # Get the full URL of the uploaded image
    blob_url = blob_client.url
    print(blob_url,"blob_url")

    return blob_name



def save_video_to_azure(video_data, _id, name, entity_type):
    try:
        # Decode base64 video
        decoded_video = base64.b64decode(video_data)
        # Create a folder name based on the provided _id and entity_type
        folder_name = str(_id)
        # Generate unique video name
        video_name = f"{name}_{uuid.uuid4().hex[:8]}.mp4"
        # Azure settings
        container_name = 'sathayush'
        folder_path = f"{entity_type}/{folder_name}/"  # Example: 'trainings/1234/'
        blob_name = f"{folder_path}{video_name}"  # Full path for the video in Azure Blob Storage
        print(blob_name, "Generated Blob Name")
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        # Upload the video to Azure Blob Storage
        blob_client.upload_blob(decoded_video, blob_type="BlockBlob", overwrite=True)
        # Instead of returning the full URL, return the relative path
        return blob_name  # Returning the relative path of the uploaded video
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print the error message for debugging
        return None




def video_path_to_binary(filename):
    if not filename:  # Check if filename is None or empty
        return None

    video_url = settings.FILE_URL

    def get_base64_encoded_video(video_path):
        if os.path.exists(video_path):
            with open(video_path, "rb") as video_file:
                video_data = video_file.read()
                base64_encoded_video = base64.b64encode(video_data)
                return base64_encoded_video.decode('utf-8')  # Return the base64 string
        else:
            return None







from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(email, otp):
    subject = "GRAMADEVATA - Account Verification OTP"
    from_email = settings.EMAIL_HOST_USER
    to = [email]

    text_content = f"Your OTP for GRAMADEVATA account verification is {otp}"

    html_content = f"""
    <html>
        <body>
            <h2>GRAMADEVATA Account Verification</h2>
            <p>Dear User,</p>
            <p>Thank you for registering with <b>GRAMADEVATA</b>.</p>
            <p>Your One-Time Password (OTP) is:</p>
            <h1 style="color:#2E86C1;">{otp}</h1>
            <p><b>Please do not share this OTP with anyone.</b></p>
            <br>
            <p>Regards,<br>Team GRAMADEVATA</p>
        </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()








# def send_email(email, otp):
#     subject = 'Your GRAMADEVATA account verification email'
#     message = f'Your OTP is {otp}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]  # Make sure to pass the email as a list
#     send_mail(subject, message, email_from, recipient_list)

    
def send_welcome_email(username):
    subject = 'Welcome to Gramadevata'
    html_content = f"""
    <html>
    <head>
        <title>Welcome to Gramadevata</title>
    </head>
    <body>
        <p>Dear {username},</p>
        <p>Namaskaram Welcome to Gramadevata Foundation,</p>
        <p>Thank you(dhanyavad) for joining Gramadevata web-app social networking platform. We are pleased to have you as a member of our community. we look forward to your valuable contributions as a part of our mission to bring people together in our community. Your support allow us to continue fulfil our mission and serve Hindu society.</p>
        <p>Please feel free to share the information about your village-area, temple, goshala and events by uploading in Gramadevata web-app platform</p>
        <p>If you have any queries or require assistance, please feel free to contact our moderation team infogd@sathayushtech.com</p>
        <p>Best Regards,<p>
        <p>Gramadevata Foundation</p>
    </body>
    </html>
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [username]
    send_mail(
        subject=subject,
        message='',
        from_email=email_from,
        recipient_list=recipient_list,
        html_message=html_content
    )




from azure.storage.blob import BlobServiceClient, ContentSettings
import uuid


def save_audio_to_azure(audio_file, _id, name, entity_type):
    # Handle base64 or raw audio file
    if isinstance(audio_file, str):
        try:
            decoded_audio = base64.b64decode(audio_file)
        except base64.binascii.Error:
            raise ValueError("Invalid base64 audio data.")
    elif hasattr(audio_file, 'read'):  # Assuming file-like object (e.g., uploaded file)
        decoded_audio = audio_file.read()
    else:
        raise ValueError("Unsupported audio format. Provide base64 string or file object.")

    # Create folder name based on _id and entity_type
    folder_name = str(_id)

    # Generate unique audio name
    audio_name = f"{name}_{uuid.uuid4().hex[:8]}.mp3"

    # Azure Blob Storage settings
    container_name = 'sathayush'
    folder_path = f"{entity_type}/{folder_name}/"  # Example: 'news/1234/'
    blob_name = f"{folder_path}{audio_name}"  # Full path for the audio in Azure Blob Storage

    # Initialize BlobServiceClient using connection string from settings
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Upload the audio to Azure Blob Storage with proper Content-Type
        blob_client.upload_blob(
            decoded_audio, 
            blob_type="BlockBlob", 
            overwrite=True, 
            content_settings=ContentSettings(content_type="audio/mpeg")  # Set Content-Type
        )

        # Get the full URL of the uploaded audio
        blob_url = blob_client.url
        return blob_name
    except Exception as e:
        # Log the error and re-raise for further handling
        raise RuntimeError(f"Error uploading audio to Azure: {str(e)}")




import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_location_from_ip(ip):
    # Localhost / private IP fallback
    if ip in ["127.0.0.1", "localhost"]:
        return {"country": None, "state": None, "city": None}

    try:
        response = requests.get(
            f"https://ipapi.co/{ip}/json/",
            timeout=3
        )
        data = response.json()

        return {
            "country": data.get("country_name"),
            "state": data.get("region"),
            "city": data.get("city"),
        }
    except Exception:
        return {"country": None, "state": None, "city": None}






import threading

def run_async(func, *args, **kwargs):
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()










def save_image_to_azure1(image_data, _id, name, entity_type):
    # Decode base64 image
    decoded_image = base64.b64decode(image_data)
    
    # Create a folder name based on the provided _id and entity_type
    folder_name = str(_id)
    
    # Generate unique image name
    image_name = f"{name}_{uuid.uuid4().hex[:8]}.webp"
    
    # Azure settings
    container_name = 'sathayush'
    folder_path = f"{entity_type}/{folder_name}/"  # Example: 'temple/1234/'
    blob_name = f"{folder_path}{image_name}"  # Full path for the image in Azure Blob Storage
    print(blob_name,"3efrgth")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the image to Azure Blob Storage
    blob_client.upload_blob(decoded_image, blob_type="BlockBlob", overwrite=True)

    # Get the full URL of the uploaded image
    blob_url = blob_client.url
    print(blob_url,"blob_url")

    return blob_name









from django.core.mail import send_mail
from django.conf import settings

def send_membership_reminder(user):
    subject = "Become a Member & Add Your Contributions"
    message = f"""
Dear {user.full_name},

You are currently not a member.

Please become a member and add:
- Temples
- Events
- Goshalas (if any)

Your contribution helps preserve our culture and heritage.

Thank you,
Gramadevata Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True
    )







from django.utils import timezone
from datetime import timedelta

def get_user_activity_status(user):
    if not user.last_seen:
        return "INACTIVE"

    if user.last_seen >= timezone.now() - timedelta(minutes=5):
        return "ACTIVE"

    return "INACTIVE"
