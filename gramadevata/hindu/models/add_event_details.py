from django.db import models
import uuid
from ..models import Event,Register
from django.utils import timezone
from ..enums import *
class AddEventDetails(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True,default=list)
    desc = models.TextField(db_column='desc', blank=True, null=True)
    map_location = models.URLField(db_column='map_location', blank=True, null=True)
    event_id = models.ForeignKey(Event, db_column='event_id',  on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True,db_index=True)
    start_time = models.TimeField(db_column='start_time', null=True, blank=True)
    end_time = models.TimeField(db_column='end_time', null=True, blank=True)
    event_video = models.JSONField(db_column='event_video', null=True, blank=True, default=list)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)

    class Meta:
        managed = True
        db_table = 'add_event_details'
        ordering = ['-created_at']