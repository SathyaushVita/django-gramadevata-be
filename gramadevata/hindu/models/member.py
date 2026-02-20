from django.db import models
from ..enums.villager_role_enum import VillagerRole
import uuid
from ..models import *


class MemberModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(max_length=200,db_index=True)
    surname = models.CharField(max_length = 200)
    father_name = models.CharField(max_length = 200)
    you_belongs_to_the_village = models.CharField(max_length = 200, null=True, blank=True)
    your_role_in_our_village = models.CharField(max_length=200, choices=[(e.name,e.value)for e in VillagerRole], default=VillagerRole.Villager.value)
    contact_number = models.CharField(max_length = 100)
    user = models.ForeignKey(Register, db_column="user", on_delete=models.CASCADE, related_name='Member', blank=True, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True,related_name="Member",db_column='village',db_index=True)
    connect = models.ForeignKey(ConnectModel, on_delete=models.CASCADE,null =True,blank=True,related_name="Member",db_column="connect",db_index=True)
    pujari_certificate = models.TextField(db_column='pujari_certificate',null=True,blank=True)
    working_temple = models.CharField(db_column='working_temple',max_length=150, null=True, blank=True)


    class Meta:
        db_table = "Member"



    


