import uuid
from django.db import models
from ..enums import *
from .village import Village
from .register import Register

class Geographic(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    ancient_name = models.CharField(db_column='ancient_name', max_length=100,blank=True, null=True,db_index=True)
    # other_name = models.CharField(db_column='other_name', max_length=45,blank=True, null=True)
    geographic_location = models.CharField(db_column='geographic_location',max_length=50,choices=[(e.value, e.name) for e in GeographicLocation],blank=True,null=True) 
    primary_language = models.CharField(db_column="primary_language",max_length=1000,blank=True, null=True)
    languages = models.CharField(db_column='languages', max_length=45,blank=True, null=True)
    population = models.CharField(db_column='population', max_length=45,blank=True, null=True)
    male_population = models.CharField(db_column='male_population', max_length=45,blank=True, null=True)
    female_population = models.CharField(db_column='female_population', max_length=45,blank=True, null=True)
    others_population = models.CharField(db_column='others_population', max_length=45,blank=True, null=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='geographic')
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id', on_delete=models.SET_NULL, related_name='geographic', blank=True, null=True,db_index=True)
    map_location = models.URLField(db_column='map_location', max_length=4500, blank=True, null=True) 
    under_panchayat = models.CharField(db_column='under_panchayat', max_length=100,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'village_geographic_and_demographic'
        ordering = ['-created_at']