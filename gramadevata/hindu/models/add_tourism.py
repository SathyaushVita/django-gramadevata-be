import uuid
from django.db import models
from ..models import Register
from ..enums import *
from .tourismplaces import TempleNearbyTourismPlace


class AddTourismPlace(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    address = models.TextField(blank=True, null=True)
    desc = models.TextField(db_column='desc', blank=True, null=True)
    type=models.CharField(max_length=255,blank=True, null=True)
    map_location = models.CharField(max_length=500, blank=True, null=True)
    image_location = models.JSONField(blank=True, null=True, default=list)
    tourism_id = models.ForeignKey(TempleNearbyTourismPlace, db_column='tourism_id', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    timings=models.CharField(max_length=255,db_column='timings',blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50,choices=[(e.name, e.value) for e in EntityStatus],default=EntityStatus.INACTIVE.value,db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "add_tourismplace"
        ordering = ['-created_at']

    def __str__(self):
        return self.tourism_place_name or ""