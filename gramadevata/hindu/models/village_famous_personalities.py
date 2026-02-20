# models.py
import uuid
from django.db import models
from ..enums import *
from .village import Village
from .register import Register

class VillageFamousPersonality(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='famous_personalities',db_index=True)
    person_name = models.CharField(db_column="person_name",max_length=255,blank=True, null=True)
    person_image= models.JSONField(db_column="person_image",blank=True,null=True)
    personal_details = models.TextField(db_column="personal_details",blank=True, null=True)
    legends_stories = models.TextField(db_column="lengends_stories",blank=True, null=True)
    person_family = models.TextField(blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id', on_delete=models.SET_NULL, related_name='famous_personalities', blank=True, null=True,db_index=True)

    class Meta:
        db_table = 'village_famous_personalities'
        ordering = ['-created_at']

    def __str__(self):
        return self.personality_name
