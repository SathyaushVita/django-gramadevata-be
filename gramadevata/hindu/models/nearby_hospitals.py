from django.db import models
import uuid
from .village import Village
from .temple import Temple 
from ..enums import *
from ..models import Register
from .event import Event
from .tourismplaces import TempleNearbyTourismPlace

class NearbyHospital(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    address = models.TextField()
    map_location = models.CharField(max_length=255,null=True, blank=True) 
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='near_by_hospitals', db_column="temple_id", null=True, blank=True,db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='near_by_hospitals',db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='near_by_hospitals', db_column="event_id", null=True, blank=True,db_index=True)
    tourism_places = models.ForeignKey(TempleNearbyTourismPlace, db_column='tourism_places', on_delete=models.SET_NULL, null=True, blank=True,related_name='near_by_hospitals',db_index=True)
    owner_name=models.CharField(max_length=255,null=True, blank=True,db_column="owner_name")
    contact_number=models.CharField(db_column="contact_number",max_length=20,null=True, blank=True)
    license_copy = models.TextField(db_column='license_copy', blank=True, null=True)

    class Meta:
        db_table = 'nearby_hospitals'
        ordering = ['-created_at']
