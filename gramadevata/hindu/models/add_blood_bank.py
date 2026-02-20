import uuid
from django.db import models
from ..models import Register, BloodBank
from ..enums import *



class AddMoreBloodBank(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    blood_bank_id = models.ForeignKey(BloodBank,db_column='blood_bank_id',on_delete=models.CASCADE,related_name='additional_details',null=True,blank=True,db_index=True)
    user_id = models.ForeignKey(Register,db_column='user_id',on_delete=models.CASCADE,null=True,blank=True,db_index=True)
    desc = models.TextField(blank=True, null=True)
    image_location = models.JSONField(blank=True, null=True, default=list)
    license_copy = models.TextField(blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50,choices=[(e.name, e.value) for e in EntityStatus],default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "add_more_blood_bank"
        ordering = ['-created_at']

    def __str__(self):
        return f"Additional Details for {self.blood_bank_id.name if self.blood_bank_id else ''}"
