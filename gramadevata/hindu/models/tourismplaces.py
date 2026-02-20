from django.db import models
import uuid
from .temple import Temple
from .village import Village
from ..enums import *
from ..models import Register,Goshala
from .country import Country




class TempleNearbyTourismPlace(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    name = models.CharField(max_length=255,null=True, blank=True,db_index=True)
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='tourismplace',db_column="temple_id",null=True, blank=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    address = models.TextField(null=True, blank=True)
    map_location = models.CharField(max_length=255,null=True, blank=True)
    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True,related_name='tourismplace',db_index=True)
    status = models.CharField(db_column='status', max_length=50 ,choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,db_index=True)
    image_location = models.TextField(db_column='image_location', blank=True, null=True)
    desc=models.TextField(null=True, blank=True)
    timings=models.CharField(db_column="timings",max_length=100,null=True,blank=True)
    type=models.CharField(db_column="type",max_length=100,null=True,blank=True)
    goshala_id = models.ForeignKey(Goshala, on_delete=models.CASCADE, related_name='tourismplace',db_column="goshala_id",null=True, blank=True,db_index=True)
    country = models.ForeignKey(Country,related_name="tourismplace",on_delete=models.CASCADE,blank=True, null=True,db_index=True,db_column="country")
    contact_number = models.CharField(db_column="contact_number",max_length=20, blank=True, null=True)
    email = models.EmailField(db_column="email",blank=True, null=True)
    class Meta:
        db_table = 'temple_nearby_tourismplaces'
