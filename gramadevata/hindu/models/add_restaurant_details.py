from django.db import models
import uuid
from ..models import Goshala,Register
from django.utils import timezone
from ..enums import *
from .resturents import TempleNearbyRestaurant

class AddRestaurantDetails(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True,default=list)
    map_location = models.URLField(db_column='map_location', blank=True, null=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True,db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    name = models.CharField(max_length=255,null=True, blank=True,db_index=True)
    address = models.TextField(null=True, blank=True,db_column="address")
    owner_name=models.CharField(max_length=255,db_column='owner_name', blank=True, null=True)
    contact_number=models.CharField(db_column='contact_number',max_length=20,blank=True, null=True)
    email_id=models.CharField(db_column='email_id',max_length=100,blank=True, null=True)
    website = models.URLField(db_column='website', max_length=255, blank=True, null=True)
    restaurent_id = models.ForeignKey(TempleNearbyRestaurant, db_column='restaurent_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='add_more_resturents',db_index=True)

    class Meta:
        managed = True
        db_table = 'add_restaurent_details'
        ordering = ['-created_at']