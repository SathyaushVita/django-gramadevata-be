from django.db import models
import uuid
from ..models import Temple,Register
from django.utils import timezone


from ..enums import *



class AddTempleDetails(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    image_location = models.JSONField(db_column='image_location', blank=True, null=True,default=list)
    desc = models.TextField(db_column='desc', blank=True, null=True)
    map_location = models.URLField(db_column='map_location', blank=True, null=True)
    temple_id = models.ForeignKey(Temple, db_column='temple_id',  on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True,db_index=True)
    temple_website = models.URLField(db_column='temple_website', blank=True, null=True)
    video = models.JSONField(db_column='video', null=True, blank=True, default=list) 
    temple_area = models.CharField(db_column='temple_area', max_length=100, blank=True, null=True)
    temple_timings = models.CharField(db_column='temple_timings', max_length=100, blank=True, null=True)
    construction_year = models.CharField(max_length=100,db_column='construction_year', blank=True, null=True)
    other_diety = models.CharField(db_column='other_diety', blank=True, null=True, max_length=100)  
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)



    class Meta:
        managed = True
        db_table = 'add_temple_details'
        ordering = ['-created_at']