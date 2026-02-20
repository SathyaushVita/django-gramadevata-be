
from django.db import models
import uuid
from .temple import Temple
from .register import Register  # or your custom user model
from ..enums import ActivityOption, EntityStatus

class PrayersAndBenefits(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='prayers_and_benefits', db_column='temple_id',db_index=True)
    user_id = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='prayers', db_column='user_id',db_index=True)

    homam = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    special_vratas = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    sevas = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    abshikam = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    kalyanam = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)

    status = models.CharField(max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        db_table = "prayers_and_benefits"
        ordering = ['-created_at']
