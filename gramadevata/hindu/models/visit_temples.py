import uuid
from django.db import models
from .temple import Temple
from ..models import Register
from .goshala import Goshala
from .event import Event

class VisitTemple(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False)
    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.CASCADE, null=True, blank=True,related_name='visit_temples')
    temple_id = models.ForeignKey(Temple, on_delete=models.CASCADE, related_name='visit_temples', db_column="temple_id", null=True, blank=True)
    goshala_id = models.ForeignKey(Goshala, on_delete=models.CASCADE, related_name='visit_goshalas', db_column="goshala_id", null=True, blank=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='visit_events', db_column="event_id", null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        db_table = 'visited_temples'
        # unique_together = ('user_id', 'temple_id') 
        ordering = ['-created_at']
