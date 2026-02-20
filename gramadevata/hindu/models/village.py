
import uuid
from django.db import models
from ..models import *
# from .goshala import Goshala
from django.contrib.contenttypes.fields import GenericRelation
from ..enums import EntityStatus
from .register import Register
# from .temple import Temple
from django.dispatch import receiver
from ..enums import GeographicLocation
from ..utils import *
from .block import Block

class Village(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length=45,db_index=True) 
    desc = models.TextField(db_column='desc', blank=True, null=True, default=None)
    mapUrl = models.URLField(db_column='map_url', max_length=255, null=True, blank=True)  
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.value, e.name) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    pin_code = models.CharField(db_column='pin_code', max_length=15) 
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='villages',db_column="block_id",db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)    
    image_location= models.JSONField(max_length=500, null=True, blank=True,default=list)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, related_name='villages',null=True,db_index=True)   
    type=models.CharField(db_column='type', max_length=30, choices=[('VILLAGE','VILLAGE'),('AREA','AREA')],default='VILLAGE',blank=True)    
    old_village_code = models.CharField(db_column='old_village_code', max_length=45, null=True)
    village_video = models.JSONField(db_column='village_video', blank=True, null=True,default=list)
    precedence=models.IntegerField(db_column="precedence",null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)





    class Meta:
        managed = True
        db_table = 'village'

