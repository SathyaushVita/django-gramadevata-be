import uuid
from django.db import models
from django.conf import settings
from ..models import Register
from .temple import Temple
from .village import Village
from ..enums import *
from .event import Event

class TourOperator(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)
    tour_operator_name = models.CharField(max_length=255,blank=True, null=True,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='touroperator', db_column="temple_id", null=True, blank=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    rating = models.CharField(blank=True, null=True,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    mobile_number = models.CharField(max_length=15,blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='touroperator',db_index=True)
    contact_address = models.TextField(blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    map_location = models.CharField(max_length=500,null=True, blank=True) 
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='touroperator', db_column="event_id", null=True, blank=True,db_index=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True)

    class Meta:
        db_table = "tour_operator"
        ordering = ['-created_at']

    def __str__(self):
        return self.tour_operator_name
