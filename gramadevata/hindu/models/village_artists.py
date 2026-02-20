# models.py
import uuid
from django.db import models
from ..enums import *
from .village import Village
from .register import Register

class VillageArtist(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='village_artists',db_index=True)
    artist_name = models.CharField(db_column="artist_name",max_length=255,null=True,blank=True,db_index=True)
    artist_image=models.JSONField(db_column="artist_image",null=True,blank=True)
    traditional_occupation = models.TextField(blank=True, null=True)
    traditional_occupation_pics = models.JSONField(db_column='traditional_occupation_pics', blank=True, null=True)
    traditional_occupation_video = models.JSONField(db_column='traditional_occupation_video', blank=True, null=True)
    trained_under = models.TextField(blank=True, null=True)
    trained_under_pics = models.JSONField(db_column='trained_under_pics', blank=True, null=True)
    other_artists_list = models.TextField(blank=True, null=True)
    # investigator_name = models.CharField(max_length=255,blank=True, null=True)
    # investigator_contact_num = models.CharField(max_length=15,blank=True, null=True)
    audio_recordings = models.JSONField(db_column='audio_recordings', blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id', on_delete=models.SET_NULL, related_name='village_artists', blank=True, null=True)

    class Meta:
        db_table = 'village_artists'
        ordering = ['-created_at']
        

    def __str__(self):
        return self.name
