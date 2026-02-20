import uuid
from django.db import models
from ..enums import *
from .temple_categeory import *
from . temple_priority import TemplePriority
from .register import Register
from .village import Village
from .country import Country

class Temple(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    category = models.ForeignKey(TempleCategory, db_column='category', on_delete=models.SET_NULL, null=True, blank=True, related_name='temples') 
    priority = models.ForeignKey(TemplePriority, db_column='priority', on_delete=models.SET_NULL, null=True, blank=True, related_name='temples')
    name = models.CharField(db_column='name', max_length=100,null=True, blank=True,db_index=True) 
    is_navagraha_established = models.BooleanField(db_column='is_navagraha_established', blank=True, null=True, default=False) 
    construction_year = models.CharField(max_length=100,db_column='construction_year', blank=True, null=True)
    era = models.CharField(max_length=50, choices=[(e.name, e.value) for e in Era], default=None,blank=True, null=True)
    is_destroyed = models.BooleanField(db_column='is_destroyed',default=False)
    animal_sacrifice_status = models.BooleanField(db_column='animal_sacrifice_status', default=False)
    diety = models.CharField(db_column='diety', blank=True, null=True, max_length=100)  # Main Diety
    # style = models.CharField(max_length=50, choices=[(e.name, e.value) for e in TempleStyle], default=TempleStyle.OTHER.value)
    style = models.CharField(max_length=50, choices=[(e.value, e.name) for e in TempleStyle],  default=TempleStyle.OTHER.value
    )
    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value)
    object_id = models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='temples',db_index=True)
    # content_type = models.CharField(max_length=100)
    # location = models.CharField(max_length=100)
    temple_map_location = models.URLField(db_column='temple_map_location', max_length=4500, blank=True, null=True) 
    address = models.CharField(db_column='address',max_length=500, blank=True, null=True) 
    contact_name = models.CharField(db_column='contact_name', max_length=100 , blank=True, null=True) 
    contact_phone = models.CharField(db_column='contact_phone', max_length=15, blank=True, null=True)  
    contact_email = models.EmailField(db_column='contact_email', max_length=45, blank=True, null=True)
    desc = models.TextField(db_column='desc', blank=True, null=True) 
    # events = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True)
    old_temple_code = models.CharField(db_column='old_temple_code', max_length=45, null=True) 
    user = models.ForeignKey(Register,db_column='user', on_delete=models.SET_NULL, related_name='temples', null=True)
    can_connect = models.BooleanField(db_column='can_connect', blank=True, default=False)
    temple_area = models.CharField(db_column='temple_area', max_length=100, blank=True, null=True)
    temple_timings = models.CharField(db_column='temple_timings', max_length=100, blank=True, null=True)
    temple_official_website = models.URLField(db_column='temple_official_website', max_length=255, blank=True, null=True)
    other_dieties = models.CharField(db_column='other_dieties', blank=True, null=True, max_length=100)
    temple_management = models.CharField(db_column='temple_management', max_length=255, blank=True, null=True)
    sthala_vriksha = models.CharField(db_column='sthala_vriksha', max_length=100, blank=True, null=True)
    river = models.CharField(db_column='river', max_length=100, blank=True, null=True)
    ratham = models.CharField(db_column='ratham', max_length=100, blank=True, null=True)
    other_speciality = models.TextField(db_column='other_speciality', blank=True, null=True)
    sthala_puranam = models.TextField(db_column='sthala_puranam', blank=True, null=True)
    architecture = models.CharField(db_column='architecture', max_length=255, blank=True, null=True)
    longitude = models.CharField(db_column='longitude', max_length=100, blank=True, null=True)
    latitude = models.CharField(db_column='latitude', max_length=100, blank=True, null=True)
    dress_code = models.CharField(max_length=20,db_column='dress_code', choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # pooja_timings = models.CharField(db_column='pooja_timings', max_length=255, blank=True, null=True)
    festivals = models.TextField(db_column='festivals', blank=True, null=True)
    temple_video = models.JSONField(db_column='temple_video', blank=True, null=True,default=list)
    country_name=models.CharField(db_column='country_name', max_length=100, blank=True, null=True,db_index=True)
    state_name=models.CharField(db_column='state_name', max_length=100, blank=True, null=True,db_index=True)
    district_name=models.CharField(db_column='district_name', max_length=100, blank=True, null=True,db_index=True)
    block_name=models.CharField(db_column='block_name', max_length=100, blank=True, null=True,db_index=True)
    village_name=models.CharField(db_column='village_name', max_length=100, blank=True, null=True,db_index=True)
    other_name=models.CharField(db_column='other_name', max_length=100, blank=True, null=True,db_index=True)
    country = models.ForeignKey(Country,related_name="temples",on_delete=models.CASCADE,blank=True, null=True,db_index=True,db_column="country")
  


    
   
    def __str__(self):
       return self.name
   
    class Meta:
        managed = True
        db_table = 'temple'
