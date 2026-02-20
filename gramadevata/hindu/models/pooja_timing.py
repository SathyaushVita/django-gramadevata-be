from django.db import models
import uuid
from .temple import Temple
from .register import Register 
from ..enums import *

class TemplePoojaTiming(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='pooja_timing', db_column='temple_id',null=True, blank=True)
    pooja_name = models.CharField(max_length=100,db_column='pooja_name',null=True,blank=True)
    start_time = models.CharField(max_length=50,blank=True, null=True)
    end_time = models.CharField(max_length=50,blank=True, null=True)
    days = models.CharField(max_length=100)  
    desc = models.TextField(blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='pooja_timing', db_column='user_id',db_index=True)

    class Meta:
        db_table = 'temple_pooja_timings'
        ordering = ['start_time']

    def __str__(self):
        return f"{self.pooja_name} at {self.temple}"
