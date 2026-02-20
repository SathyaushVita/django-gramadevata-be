# models/village_market.py
import uuid
from django.db import models
from .village import Village
from .temple import Temple
from .register import Register
from ..enums import EntityStatus

class VillageMarket(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(max_length=255,null=True, blank=True,db_index=True)
    address = models.TextField(null=True, blank=True)
    map_location = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='markets',db_index=True)
    temple_id = models.ForeignKey(Temple, db_column='temple_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='markets',db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.SET_NULL, related_name='markets', null=True, blank=True,db_index=True)
    image_location = models.JSONField(null=True, blank=True)  
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email_id = models.CharField(max_length=100,null=True, blank=True)

    class Meta:
        db_table = 'village_market'
        ordering = ['-created_at']
