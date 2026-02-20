import uuid
from django.db import models
from ..models import *
# from .goshala import Goshala

from django.contrib.contenttypes.fields import GenericRelation
from .district import District


class Block(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length=45,db_index=True) 
    municipality = models.CharField(db_column='municipality', max_length=45, blank=True, null=True)
    population = models.CharField(db_column='population', max_length=45, blank=True, null=True)
    desc = models.TextField(db_column='desc',null=True)  
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='blocks',db_column="district_id",db_index=True)   
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    type=models.CharField(db_column='type', max_length=30, choices=[('BLOCK','BLOCK'),('TOWN','TOWN')],default='BLOCK',blank=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)

    

    class Meta:
        managed = True
        db_table = 'block'
