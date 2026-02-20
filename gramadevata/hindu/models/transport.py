from django.db import models
import uuid
from .temple import Temple
from .village import Village
from ..enums import *
from . import Register
from .event import Event
from .tourismplaces import TempleNearbyTourismPlace


class TempleTransport(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)
    desc = models.TextField(null=True, blank=True,db_collation="desc")
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='transport', db_column="temple_id", null=True, blank=True,db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='transport',db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    map_location = models.CharField(max_length=255,null=True, blank=True) 
    transport_type = models.CharField(max_length=50,choices=[(e.name, e.value) for e in TransportType],null=True, blank=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='transport', db_column="event_id", null=True, blank=True,db_index=True)
    tourism_places = models.ForeignKey(TempleNearbyTourismPlace, db_column='tourism_places', on_delete=models.SET_NULL, null=True, blank=True,related_name='transport',db_index=True)

    class Meta:
        db_table = 'temple_transport_facilities'
