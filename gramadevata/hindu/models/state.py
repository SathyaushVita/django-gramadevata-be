import uuid
from django.db import models

from .country import Country




class State(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length=45,db_index=True) 
    shortname = models.CharField(db_column='shortname', max_length=45)
    capital = models.CharField(db_column='capital', max_length=45, blank=True, null=True)
    # language = models.CharField(db_column='languagge', max_length=45, blank=True, null=True)  
    desc = models.TextField(db_column='desc', blank=True, null=True) 
    country= models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states',db_index=True,db_column="country_id")
    # country_id = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)

    type=models.CharField(db_column='type', max_length=30, choices=[('STATE','STATE')],default='STATE',blank=True)


    class Meta:
        managed = True
        db_table = 'state'


