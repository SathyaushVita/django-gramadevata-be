from django.db import models
from ..enums.villager_role_enum import VillagerRole
import uuid
from ..models import *


class PujariModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    first_name = models.CharField(max_length=200,db_index=True)
    last_name = models.CharField(max_length = 200,db_index=True)
    father_name = models.CharField(max_length = 200)
    contact_number = models.CharField(max_length = 100)
    user = models.ForeignKey(Register, db_column="user", on_delete=models.CASCADE, related_name='Pujari', blank=True, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True,related_name="Pujari",db_column='village',db_index=True)
    pujari_certificate = models.TextField(db_column='pujari_certificate',null=True,blank=True)
    working_temple = models.CharField(db_column='working_temple',max_length=150, null=True, blank=True)


    class Meta:
        db_table = "Pujari"