import uuid
from django.db import models


def unique_id_gen_evnt_catg():
    prefix = "Ecatgy"
    suffix = str(uuid.uuid4().hex)[:15]
    return "{prefix}---{suffx}"


class EventCategory1(models.Model):
    _id = models.CharField(max_length=200,db_column='_id', primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length = 45,db_index=True )
    desc = models.TextField(db_column='desc',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    pic = models.CharField(max_length=500, blank=True, null=True)
    
    
    
    # One Image
    
import uuid
from django.db import models

def unique_id_gen_evnt_catg():
    prefix = "Ecatgy"
    suffix = str(uuid.uuid4().hex)[:15]
    return f"{prefix}---{suffix}"

class EventCategory(models.Model):
    _id = models.CharField(max_length=200, db_column='_id', primary_key=True, default=unique_id_gen_evnt_catg, editable=False)
    name = models.CharField(db_column='name', max_length=45)
    desc = models.CharField(db_column='desc', blank=True, null=True, max_length=250)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    pic = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'Event_category'

