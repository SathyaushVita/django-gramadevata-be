import uuid
from django.db import models
from .state import State





class District(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length=45,db_index=True)  
    shortname = models.CharField(db_column='shortname', max_length=45)  
    headquarters = models.CharField(db_column='headquarters', max_length=45, blank=True, null=True)  
    desc = models.TextField(db_column='desc',  blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts',db_index=True,db_column="state_id")
    cityname =models.CharField(max_length=200)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)

    created_at = models.CharField(max_length = 200,db_index=True)
  
    
    type=models.CharField(db_column='type', max_length=30, choices=[('DISTRICT','DISTRICT'),('CITY','CITY')],default='DISTRICT',blank=True)

    class Meta:
        managed = True
        db_table = 'district'
