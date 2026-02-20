import uuid
from django.db import models
from .temple_main_category import TempleMainCategory

class PujariCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(db_column='name', max_length = 45,db_index=True )
 
    

    class Meta:
        db_table = 'pujari_category'
