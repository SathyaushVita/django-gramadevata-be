import uuid
from django.db import models
from ..enums import *
from .goshala_category import *
from .temple import Temple
from .register import Register
from .village import Village
from ..enums import ActivityOption, EntityStatus
from .country import Country

class Goshala(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    category = models.ForeignKey(GoshalaCategory, db_column='category', on_delete=models.SET_NULL, null=True, blank=True,db_index=True) 
    name = models.CharField(db_column='name', max_length=45,null=True, blank=True,db_index=True)
    reg_num = models.CharField(db_column='reg_num', max_length=45, blank=True, null=True) 
    status = models.CharField(db_column='status', max_length=10, blank=True, null=True,db_index=True)
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
    object_id =models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='goshalas',db_index=True)
    map_location = models.URLField(db_column='map_location', max_length=450, blank=True, null=True) 
    temple = models.OneToOneField(Temple, on_delete=models.SET_NULL, related_name='goshalas', blank=True, null=True,db_index=True)
    contact_name = models.CharField(db_column='contact_name', max_length=45, blank=True, null=True) 
    contact_phone = models.CharField(db_column='contact_phone', max_length=15, blank=True, null=True) 
    address = models.CharField(db_column='address', max_length=100,null=True, blank=True)  
    email = models.CharField(db_column='email', max_length=45, blank=True, null=True)
    desc = models.TextField(db_column='desc', blank=True, null=True)
    regn_document = models.CharField(db_column='regn_document', max_length=45, blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    # image_location = models.TextField( blank=True, null=True)
    image_location = models.JSONField( blank=True, null=True, default=list)
    user = models.ForeignKey(Register,db_column='user', on_delete=models.SET_NULL, related_name='goshalas', null=True,db_index=True)
    goshala_video = models.JSONField(db_column='goshala_video', blank=True, null=True,default=list)
    managed_by=models.CharField(db_column="managed_by",max_length=100,null=True,blank=True)
    timings=models.CharField(db_column="timings",max_length=100,null=True,blank=True)
    official_website=models.URLField(db_column='official_website', max_length=450, blank=True, null=True) 
    country_name=models.CharField(db_column='country_name', max_length=100, blank=True, null=True)
    state_name=models.CharField(db_column='state_name', max_length=100, blank=True, null=True)
    district_name=models.CharField(db_column='district_name', max_length=100, blank=True, null=True)
    block_name=models.CharField(db_column='block_name', max_length=100, blank=True, null=True)
    village_name=models.CharField(db_column='village_name', max_length=100, blank=True, null=True)
    other_name=models.CharField(db_column='other_name', max_length=100, blank=True, null=True)
    devotees_visiting = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    feeding_accessibility = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    inside_feeding_accessibility = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    outside_feeding_accessibility = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    adoption_of_cow_or_bull_inside  = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    adoption_of_cow_or_bull_outside  = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    festivals=models.CharField(db_column='festivals', max_length=100, blank=True, null=True)
    prayers=models.CharField(db_column='prayers', max_length=100, blank=True, null=True)
    social_activites=models.CharField(db_column='social_activites', max_length=100, blank=True, null=True)
    other_services=models.CharField(db_column='other_services', max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country,related_name="goshalas",on_delete=models.CASCADE,blank=True, null=True,db_index=True,db_column="country")
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)


 

    class Meta:
        managed = True
        db_table = 'goshala'
