# models.py
import uuid
from django.db import models
from ..enums import *
from .village import Village
from .register import Register
from ..enums import ActivityOption



class VillageDevelopmentFacility(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True) 
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='village_development_facilities')
    
    agriculture = models.TextField(max_length=200,null=True,blank=True,db_column="agriculture")
    handicraft = models.TextField(max_length=200,null=True,blank=True,db_column="handicraft")
    handloom = models.TextField(max_length=200,null=True,blank=True,db_column="handloom")
    smallscale_industry = models.TextField(max_length=200,null=True,blank=True,db_column="smallscale_industry")
    dairy = models.TextField(max_length=200,null=True,blank=True,db_column="dairy")
    poultry = models.CharField(max_length=200,null=True,blank=True,db_column="poultry")
    fisheries = models.CharField(max_length=200,null=True,blank=True,db_column="fisheries")
    cattle_breeding = models.CharField(max_length=200,null=True,blank=True,db_column="cattle_breeding")
    shepherding = models.CharField(max_length=200,null=True,blank=True,db_column="shepherding")
    horticulture = models.CharField(max_length=200,null=True,blank=True,db_column="horticulture")
    others = models.TextField(blank=True, null=True)

    water_and_irrigation = models.TextField(max_length=200,null=True,blank=True,db_column="water_and_irrigation")
    tap_water = models.CharField(max_length=200,null=True,blank=True,db_column="tap_water")
    toilet = models.CharField(max_length=200,null=True,blank=True,db_column="toilet")
    health_centre = models.CharField(max_length=200,null=True,blank=True,db_column="health_centre")
    school = models.CharField(max_length=200,null=True,blank=True,db_column="school")
    electricity = models.CharField(max_length=200,null=True,blank=True,db_column="electricity")
    gas = models.CharField(max_length=200,null=True,blank=True,db_column="gas")
    post_office = models.CharField(max_length=200,null=True,blank=True,db_column="post_office")
    bank = models.CharField(max_length=200,null=True,blank=True,db_column="bank")
    telephone = models.CharField(max_length=200,null=True,blank=True,db_column="telephone")
    college = models.CharField(max_length=200,null=True,blank=True,db_column="college")
    internet = models.CharField(max_length=200,null=True,blank=True,db_column="internet")
    street_drainage_system = models.TextField(max_length=200,null=True,blank=True,db_column="street_drainage_system")
    shops_and_market = models.CharField(max_length=200,null=True,blank=True,db_column="shops_and_market")
    sports_ground = models.CharField(max_length=200,null=True,blank=True,db_column="sports_ground")
    public_spaces = models.CharField(max_length=200,null=True,blank=True,db_column="public_spaces")
    road_facility = models.CharField(max_length=200,null=True,blank=True,db_column="road_facility")
    # water_and_irrigation = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # tap_water = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # toilet = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # health_centre = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # school = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # electricity = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # gas = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # post_office = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # bank = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # telephone = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # college = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # internet = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # street_drainage_system = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # shops_and_market = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # sports_ground = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # public_spaces = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    # road_facility = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)

    atm = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.SET_NULL, related_name='village_development_facilities', blank=True, null=True,db_index=True)
    bank_name= models.CharField(max_length=100,null=True,blank=True,db_column="bank_name")
    bank_contact_number= models.CharField(max_length=20,null=True,blank=True,db_column="bank_contact_number")
    primarysource_of_livelihood_image=models.JSONField(default=list,blank=True,null=True)
    class Meta:
        db_table = 'village_devlopment_facilities'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.village_id)
