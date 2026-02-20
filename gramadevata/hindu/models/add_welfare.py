
import uuid
from django.db import models
from ..enums import *
from .register import Register
from .welfare_homes import WelfareHomes





class AddWelfareHome(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(db_column='name', max_length = 45,null=True,blank=True,db_index=True)
    desc = models.TextField(db_column='desc',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    image_location = models.JSONField( blank=True, null=True,db_column="image_location")
    user = models.ForeignKey(Register, on_delete=models.SET_NULL,null=True,blank=True,db_column="user",db_index=True)   
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    address = models.CharField(db_column='address',max_length=500, blank=True, null=True) 
    website = models.URLField(blank=True, null=True)
    is_government = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value,db_column="is_government")
    established_year = models.CharField(max_length=50,blank=True, null=True,db_column="established_year")
    medical_care = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    food_and_shelter = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    counseling_services = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    rehabilitation_programs = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    skill_training = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    mental_health_support = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    legal_aid = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    is_24_7_support = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    security = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    education = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    physiotherapy = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    play_area = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    recreational_activities = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    adoption_services = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    family_counseling =models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    emergency_response = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    special_needs_support = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    map_location=models.URLField(blank=True, null=True,db_column="map_location")
    welfare_fee=models.CharField(db_column='welfare_fee',max_length=500, blank=True, null=True) 
    welfare_id=models.ForeignKey(WelfareHomes,on_delete=models.SET_NULL,null=True,blank=True,db_column="welfare_id",db_index=True)
    

    class Meta:
        db_table = 'add_welfare_homes'

    def __str__(self):
        return self.name
