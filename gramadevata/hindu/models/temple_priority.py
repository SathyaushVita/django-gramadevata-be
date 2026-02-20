import uuid
from django.db import models
import uuid
from django.db import models




import uuid
from django.db import models

class TemplePriority(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(max_length=45)  
    desc = models.TextField(blank=True, null=True)  
    shortname = models.CharField(blank=True, unique=True, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        managed = True
        db_table = 'temple_priority'


