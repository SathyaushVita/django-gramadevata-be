import uuid
from django.db import models
from ..models import Register, NearbyHospital
from ..enums import *


class AddMoreHospital(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    hospital_id = models.ForeignKey(NearbyHospital,db_column='hospital_id',on_delete=models.CASCADE,related_name='additional_details',null=True,blank=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id',on_delete=models.CASCADE,null=True,blank=True,db_index=True)
    desc = models.TextField(blank=True, null=True)
    image_location = models.JSONField(blank=True, null=True, default=list)
    address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    map_location = models.CharField(max_length=500, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email_id = models.CharField(max_length=100, blank=True, null=True)
    license_copy = models.TextField(blank=True, null=True)

    status = models.CharField(db_column='status',max_length=50,choices=[(e.name, e.value) for e in EntityStatus],default=EntityStatus.INACTIVE.value,db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "add_hospital"
        ordering = ['-created_at']

    def __str__(self):
        return f"Additional Details for {self.hospital_id.name if self.hospital_id else ''}"
