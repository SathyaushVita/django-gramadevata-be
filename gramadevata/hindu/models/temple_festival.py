# models.py
from django.db import models
import uuid
from ..enums import *
from ..models import Register
from .village import Village
from .temple import Temple 

class TempleFestival(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(max_length=255,null=True, blank=True,db_index=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='festival',db_column="temple_id",null=True, blank=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)


    class Meta:
        db_table = 'temple_festivals'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
