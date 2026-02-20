from django.db import models
import uuid
from ..models import Register
from .village import Village
from .temple import Temple
from ..enums import *
from .event import Event

class TourGuide(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='tour_guide',db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='tour_guide', db_column="temple_id", null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    tourist_spot_covered = models.TextField(db_column="tourist_spot_coverd",null=True, blank=True)
    language = models.CharField(max_length=100,null=True, blank=True)
    mobile = models.CharField(max_length=15,null=True, blank=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tour_guide', db_column="event_id", null=True, blank=True,db_index=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True)


    class Meta:
        db_table = 'tour_guides'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.village}"
