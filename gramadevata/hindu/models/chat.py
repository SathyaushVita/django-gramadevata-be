from django.db import models
from .register import Register
from .village import Village
from .temple import Temple
from django.utils.timesince import timesince
from django.utils import timezone
import uuid



class ChatModel(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45 ,default=uuid.uuid1, unique=True ,editable=False,db_index=True)
    message = models.CharField(max_length=450000,db_column="message")
    user = models.ForeignKey(Register, on_delete=models.CASCADE,  db_column='user',db_index=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, blank=True, null=True, db_column="village",db_index=True)
    created_at=models.DateTimeField(auto_now_add=True,db_index=True)
    posted_time_ago = models.CharField(db_column='posted_time_ago', max_length=255,blank=True)
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE, blank=True, null=True, db_column="temple",db_index=True)
    chat_user_type = models.CharField(db_column='chat_user_type',max_length=10,null=True,blank=True)
    chat_entity_type = models.CharField(db_column='chat_entity_type', max_length=10,null=True,blank=True)

    

    @property
    def relative_time(self):
        return timesince(self.created_at, timezone.now())

    class Meta:
        managed = True
        db_table = 'chat'
        ordering = ['-created_at']