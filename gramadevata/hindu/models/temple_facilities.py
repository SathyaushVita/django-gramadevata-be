from django.db import models
from ..enums import ActivityOption, EntityStatus
import uuid
from .temple import Temple
from ..models import Register


class TempleFacilities(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='temple_facilities', db_column="temple_id", null=True, blank=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    pooja_shops = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    restroom = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    drinking_water = models.CharField(max_length=20, db_column="drinking_water", choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    accommodation = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    restaurants = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    lockers = models.CharField(max_length=20, db_column="lockers_for_mobile/electronic_goods/bags", choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    shoe_rack = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    physical_disabilities_services = models.CharField(max_length=20, db_column="physical_disabilities_services(wheelchair)", choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    medical_emergency = models.CharField(max_length=20,db_column="medical_emergency", choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    chemist_pharmacy = models.CharField(max_length=20,db_column="chemist/pharmacy", choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        db_table = "temple_facilities"
        ordering = ['-created_at']
