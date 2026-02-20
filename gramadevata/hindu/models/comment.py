import uuid
from django.db import models
from . import *
from .register import Register
from .temple import Temple
from .goshala import Goshala
from django.utils.timesince import timesince
from .event import Event
import uuid
from django.db import models
from django.utils import timezone
from ..enums import CommentStatus



class CommentModel(models.Model):
    _id = models.UUIDField(db_column='_id', primary_key=True, default=uuid.uuid4, editable=False,db_index=True)
    temple = models.ForeignKey(Temple, db_column="temple", on_delete=models.CASCADE, related_name='comments', blank=True, null=True,db_index=True) 
    user = models.ForeignKey(Register, db_column="user", on_delete=models.CASCADE, related_name='comments', blank=True, null=True,db_index=True) 
    goshala = models.ForeignKey(Goshala, db_column="goshala", on_delete=models.CASCADE, related_name='comments', blank=True, null=True,db_index=True)
    event = models.ForeignKey(Event, db_column="event", on_delete=models.CASCADE, related_name='comments', blank=True, null=True) 
    body = models.CharField(db_column='body', max_length=250)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    # posted_time_ago = models.CharField(db_column='posted_time_ago', max_length=255,blank=True)
    status = models.CharField(db_column='status',max_length=50, choices=[(e.name, e.value) for e in CommentStatus], default=CommentStatus.ACTIVE.value)
    

    @property
    def relative_time(self):
        return timesince(self.created_at, timezone.now())
    

    class Meta:
        managed = True
        db_table = 'comment'
        ordering = ['-created_at'] 

