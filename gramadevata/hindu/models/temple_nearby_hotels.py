from django.db import models
import uuid
from .temple import Temple
from ..enums import *
from ..models import Register
from .village import Village
from .event import Event
from .tourismplaces import TempleNearbyTourismPlace


class TempleNearbyHotel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(max_length=255,null=True, blank=True,db_column="name",db_index=True)
    hotel_rating = models.CharField(null=True, blank=True,max_length=100)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='nearby_hotels',db_column="temple_id",null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    address = models.TextField(null=True, blank=True)
    map_location = models.CharField(max_length=255,null=True, blank=True)  
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='nearby_hotels',db_index=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)
    owner_name=models.CharField(max_length=255,db_column='owner_name', blank=True, null=True)
    contact_number=models.CharField(db_column='contact_number',max_length=20,blank=True, null=True)
    email_id=models.CharField(db_column='email_id',max_length=10,blank=True, null=True)
    website = models.URLField(db_column='website', max_length=255, blank=True, null=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='nearby_hotels', db_column="event_id", null=True, blank=True,db_index=True)
    tourism_places = models.ForeignKey(TempleNearbyTourismPlace, db_column='tourism_places', on_delete=models.SET_NULL, null=True, blank=True,related_name='nearby_hotels',db_index=True)
    license_copy = models.TextField(db_column='license_copy', blank=True, null=True)
    restaurent = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)

    class Meta:
        db_table = 'temple_nearby_hotels'
        ordering = ['-created_at']

    def __str__(self):
        return self.name