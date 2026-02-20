from django.db import models
from ..models import Temple
from ..models import Village

from ..enums.connected_enum import ConnectedAs
import uuid
from ..models import Register


class ConnectModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    user = models.ForeignKey(Register, on_delete=models.CASCADE,null =True,blank=True, related_name='Connections', db_column='user',db_index=True)
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, null=True,blank=True, related_name="Connections",db_column='temple')
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True,related_name="Connections",db_column='village')
    description = models.TextField(null=True, blank=True,db_column='description')
    connected_as = models.CharField(max_length=30, choices=[(e.value, e.name) for e in ConnectedAs], default=ConnectedAs.MEMBER.value)
    belongs_as = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)


    class Meta:
        db_table="connect"