import uuid
from django.db import models
from .pujari_category import PujariCategory

class PujariSubCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45,default=uuid.uuid1, unique=True, editable=False,db_index=True)
    name = models.CharField(db_column='name', max_length=100,db_index=True)
    category = models.ForeignKey(PujariCategory, on_delete=models.CASCADE,db_column='category_id', related_name='subcategories',db_index=True)

    class Meta:
        db_table = 'pujari_sub_category'
