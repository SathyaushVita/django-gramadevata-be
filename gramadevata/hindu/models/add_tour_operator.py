import uuid
from django.db import models
from ..models import Register
from ..enums import *
from .tour_operator import TourOperator


class AddTourOperator(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    tour_operator_name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    rating = models.CharField(blank=True, null=True, max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_address = models.TextField(blank=True, null=True)
    map_location = models.CharField(max_length=500, blank=True, null=True)
    image_location = models.JSONField(blank=True, null=True, default=list)
    tour_operator_id = models.ForeignKey(TourOperator, db_column='tour_operator_id', on_delete=models.CASCADE, null=True, blank=True, db_index=True)

    status = models.CharField(db_column='status', max_length=50,choices=[(e.name, e.value) for e in EntityStatus],default=EntityStatus.INACTIVE.value,db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "add_tour_operator"
        ordering = ['-created_at']

    def __str__(self):
        return self.tour_operator_name or ""
