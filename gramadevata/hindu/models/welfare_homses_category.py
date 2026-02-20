import uuid
from django.db import models

class WelfareHomesCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(db_column='name', max_length = 45,null=True,blank=True,db_index=True)
    desc = models.TextField(db_column='desc',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    image_location = models.CharField(max_length=500, blank=True, null=True,db_column="image_location")
    priority = models.IntegerField(null=True, blank=True, db_column='priority')

    class Meta:
        db_table = 'welfare_homes_category'
