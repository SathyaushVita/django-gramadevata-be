from django.db import models
import uuid
from ..models import Temple,Village,Register
from ..enums import *



class Media(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)
    title = models.TextField(db_column='title', null=True, blank=True,db_index=True)
    desc = models.TextField(db_column='desc', null=True, blank=True)  
    video = models.JSONField(db_column='video', null=True, blank=True, default=list)  
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True)
    temple_id = models.ForeignKey(Temple, db_column='temple_id', on_delete=models.CASCADE, null=True, blank=True,related_name='media',db_index=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.CASCADE, null=True, blank=True,related_name='media',db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)


    class Meta:
        db_table = 'media'



