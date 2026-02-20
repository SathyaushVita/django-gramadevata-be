import uuid
from django.db import models
from ..models import Register, PoojaStore
from ..enums import *



class AddMorePoojaStore(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    pooja_store_id = models.ForeignKey(PoojaStore,db_column='pooja_store_id',on_delete=models.CASCADE,related_name='additional_details',null=True,blank=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id',on_delete=models.CASCADE,null=True,blank=True,db_index=True)
    desc = models.TextField(blank=True, null=True)
    image_location = models.JSONField(blank=True, null=True, default=list)
    address = models.TextField(blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    map_location = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(db_column='status',max_length=50,choices=[(e.name, e.value) for e in EntityStatus],default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "add_more_pooja_store"
        ordering = ['-created_at']

    def __str__(self):
        return f"Additional Details for {self.pooja_store_id.name if self.pooja_store_id else ''}"
