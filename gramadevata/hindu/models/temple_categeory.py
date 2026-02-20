import uuid
from django.db import models
from .temple_main_category import TempleMainCategory

class TempleCategory(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True) 
    name = models.CharField(db_column='name', max_length = 45,db_index=True)
    desc = models.TextField(db_column='desc',blank=True, null=True)
    shortname = models.CharField(db_column='shortname', blank=True, unique=True, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    
    # One Image
    pic = models.CharField(max_length=500, blank=True, null=True)
    main_category = models.ForeignKey(
        TempleMainCategory,
        on_delete=models.CASCADE,
        related_name='temple_categories',
        db_column='main_category_id'
    )
    

    class Meta:
        db_table = 'temple_category'
