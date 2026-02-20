from django.db import models
import uuid
from .village import Village
from .temple import Temple 
from ..enums import *
from ..models import Register
from .goshala import Goshala

class VeterinaryHospital(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(max_length=255,db_index=True)
    address = models.TextField()
    map_location = models.CharField(max_length=1000, blank=True, null=True)
    image_location = models.JSONField( blank=True, null=True, default=list)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='vetarnary_hospital', db_column="temple_id", null=True, blank=True,db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='vetarnary_hospital',db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    goshala_id = models.ForeignKey(Goshala, on_delete=models.CASCADE, related_name='vetarnary_hospital', db_column="goshala_id", null=True, blank=True,db_index=True)
    desc = models.TextField(blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    contact_number=models.CharField(db_column="contact_number",max_length=20,null=True, blank=True)
    license_copy = models.TextField(db_column='license_copy', blank=True, null=True)
    class Meta:
        db_table = 'nearby_vetarnary_hospital'
        ordering = ['-created_at']
