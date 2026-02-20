import uuid
from django.db import models

class TempleMainCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(db_column='name', max_length = 45 )
    desc = models.TextField(db_column='desc',blank=True, null=True)
    shortname = models.CharField(db_column='shortname', blank=True, unique=True, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    pic = models.CharField(max_length=500, blank=True, null=True,db_column="pic")
    

    class Meta:
        db_table = 'main_category'
