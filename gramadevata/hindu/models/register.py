from django.db import models
from ..enums.user_status_enum import UserStatus
import uuid
# import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from ..utils import send_email,generate_otp,validate_email,send_sms
from django.dispatch import receiver
from django.db.models.signals import post_save
from ..enums import AccountType,MemberType,MemberStatus,MaritalStatus,StakeholderType
from ..enums.gender_enum import Gender
from ..enums import *
# from .pujari_category import PujariCategory
from .pujari_category import PujariCategory
from .pujari_subcategory import PujariSubCategory


class Register(AbstractUser):
    id = models.CharField(db_column='id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True) 
    full_name = models.CharField(db_column='full_name',max_length=200,blank=True, null=True)
    surname = models.CharField(db_column='surname', max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=200,db_column='first_name')
    last_name = models.CharField(max_length=200,db_column='last_name')
    contact_number=models.CharField(db_column='contact_number',max_length=10)
    profile_pic= models.TextField(db_column='profile_pic',blank=True, null=True)
    gender = models.CharField(max_length=50,db_column='gender',choices=[(e.name, e.value) for e in Gender],null=True,blank=True)
    dob = models.DateField()
    gotram = models.CharField(db_column='gotram',max_length=200, blank=True,null=True) 
    verification_otp = models.CharField(max_length=6, null=True, blank=True,db_index=True)
    verification_otp_created_time = models.DateTimeField(null=True)
    verification_otp_resend_count = models.IntegerField(default=0)
    status = models.CharField(db_column='status',max_length=50, choices=[(e.name, e.value) for e in UserStatus], default=UserStatus.CREATED.value)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank =True)
    forgot_password_otp_created_time = models.DateTimeField(null=True,db_index=True)
    forgot_password_otp_resend_count = models.IntegerField(default=0)
    is_member=models.CharField(db_column='is_member',max_length=50,choices=[(e.name,e.value) for e in MemberStatus],default=MemberStatus.false.value)
    type=models.CharField(db_column="type",max_length=50,choices=[(e.name,e.value) for e in MemberType],default=MemberType.MEMBER.value)
    pujari_certificate = models.JSONField(db_column='pujari_certificate', null=True, blank=True, default=list)
    working_temple = models.CharField(db_column='working_temple',max_length=150, null=True, blank=True)
    family_images = models.JSONField(db_column='family_images',default=list)
   #father side
    father_name=models.CharField(db_column='father_name',max_length=200)
    paternal_grandfather_name=models.CharField(db_column='paternal_grandfather_name',max_length=200, null=True, blank=True)
    paternal_grandmother_name=models.CharField(db_column='paternal_grandmother_name',max_length=200, null=True, blank=True)
    # Great Grandparents (Father's Father's Side)
    paternal_great_grandfather_name=models.CharField(db_column='paternal_great_grandfather_name',max_length=200, null=True, blank=True)
    paternal_great_grandmother_name=models.CharField(db_column='paternal_great_grandmother_name',max_length=200, null=True, blank=True)
    # Great Grandparents (Father's Mother's Side):
    paternal_grandmother_father_name=models.CharField(db_column='paternal_grandmother_father_name',max_length=200, null=True, blank=True)
    paternal_grandmother_mother_name=models.CharField(db_column='paternal_grandmother_mother_name',max_length=200, null=True, blank=True)
    # Mother's Side
    mother_name=models.CharField(db_column='mother_name',max_length=200, null=True, blank=True)
    maternal_grandfather_name=models.CharField(db_column='maternal_grandfather_name',max_length=200, null=True, blank=True)
    maternal_grandmother_name=models.CharField(db_column='maternal_grandmother_name',max_length=200, null=True, blank=True)
    # Great Grandparents (Mother's Father's Side):
    maternal_great_grandfather_name=models.CharField(db_column='maternal_great_grandfather_name',max_length=200, null=True, blank=True)
    maternal_great_grandmother_name=models.CharField(db_column='maternal_great_grandmother_name',max_length=200, null=True, blank=True)
    # Great Grandparents (Mother's Mother's Side):
    maternal_grandmother_father_name=models.CharField(db_column='maternal_grandmother_father_name',max_length=200, null=True, blank=True)
    maternal_grandmother_mother_name=models.CharField(db_column='maternal_grandmother_mother_name',max_length=200, null=True, blank=True)
    account_type = models.CharField(db_column='account_type',max_length=100,choices=[(e.name, e.value) for e in AccountType],default=AccountType.PRIVATE.value)
    marital_status = models.CharField(db_column='marital_status',max_length=100,choices=[(e.name, e.value) for e in MaritalStatus],null=True,blank=True)
    wife = models.CharField(db_column='wife', max_length=100,null=True, blank=True)
    husband = models.CharField(db_column='husband', max_length=100,null=True, blank=True)
    children = models.CharField(db_column='children', max_length=500,null=True, blank=True)
    siblings = models.CharField(db_column='siblings', max_length=500,null=True, blank=True)
    pujari_designation = models.CharField(max_length=500,null=True, blank=True)
    stakeholder_type = models.CharField(max_length=50, choices=[(e.name, e.value) for e in StakeholderType], default=StakeholderType.NONE.value)
    is_staff=models.BooleanField(db_column='is_staff',default=False, null=True,blank=True)
    voluntary_level = models.CharField(max_length=50,choices=[(e.name, e.value) for e in GeoSite],null=True,blank=True,db_column="voluntary_level")
    pujari_expertise=models.CharField(db_column='pujari_expertise', max_length=500,null=True, blank=True)
    pujari_id_type = models.CharField(db_column='pujari_id_type',max_length=50,choices=[(e.name, e.value) for e in PujariIdType],null=True,blank=True)
    pujari_id_image=models.TextField(db_column="pujari_id_image",null=True,blank=True)
    pujari_certificate_type = models.CharField(db_column='pujari_certificate_type',max_length=50,choices=[(e.name, e.value) for e in PujariCertificateType],null=True,blank=True)
    pujari_category = models.ManyToManyField(PujariCategory, related_name="pujari_set")
    pujari_sub_category = models.ManyToManyField(PujariSubCategory, related_name="pujari_set")
    issued_by = models.CharField(db_column='issued_by',max_length=50,choices=[(e.name, e.value) for e in PujariCertificate],null=True,blank=True)
    pujari_type = models.CharField(db_column='pujari_type',max_length=50,choices=[(e.name, e.value) for e in PujariType],null=True,blank=True)
    pujari_video = models.JSONField(db_column='pujari_video', null=True, blank=True, default=list)  
    mf_image=models.JSONField(db_column='mf_image', null=True, blank=True, default=list)  
    f_mf_image=models.JSONField(db_column='f_mf_image', null=True, blank=True, default=list)  
    m_mf_image=models.JSONField(db_column='m_mf_image', null=True, blank=True, default=list)  
    ff_mf_image=models.JSONField(db_column='ff_mf_image', null=True, blank=True, default=list)  
    fm_mf_image=models.JSONField(db_column='fm_mf_image', null=True, blank=True, default=list)  
    mf_mf_image=models.JSONField(db_column='mf_mf_image', null=True, blank=True, default=list)  
    mm_mf_image=models.JSONField(db_column='mm_mf_image', null=True, blank=True, default=list)  
    desc=models.TextField(db_column="desc",null=True, blank=True,)
    last_seen = models.DateTimeField(null=True, blank=True)
    active_count = models.IntegerField(db_column='active_count', default=0)
    inactive_count = models.IntegerField(db_column='inactive_count', default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    # last_login= models.DateTimeField(null=False, default=timezone.now, db_index=True)

    class Meta:
        db_table = "user"

    
    def __str__(self):
        return self.username




# @receiver(post_save, sender=Register)
# def send_email_or_sms_token(sender, instance, created, **kwargs):
#     if created:
#         try:
#             username = instance.username
#             if validate_email(username):
#                 otp = generate_otp()
#                 instance.verification_otp = otp
#                 instance.verification_otp_created_time = timezone.now()
#                 instance.save()
#                 send_email(username, otp)
#             else: 
#                 otp = generate_otp()
#                 instance.verification_otp = otp
#                 instance.verification_otp_created_time = timezone.now()
#                 instance.save()
#                 send_sms(username, otp)
#         except Exception as e:
#             print(f"An error occurred while sending verification token: {e}")








