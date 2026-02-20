# models.py
import uuid
from django.db import models
from ..enums import *
from .village import Village
from .register import Register



class VillageCulturalProfile(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)

    village_id = models.ForeignKey(Village, db_column='village_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='village_cultural_profile',db_index=True)
    
    famous_for = models.TextField(db_column='famous_for', blank=True, null=True)
    religious_beliefs = models.TextField(db_column='religious_beliefs', blank=True, null=True)
    religios_beliefs_image = models.JSONField(db_column='religios_beliefs_image', blank=True, null=True)
    traditional_food = models.TextField(db_column='traditional_food', blank=True, null=True)
    traditional_food_image = models.JSONField(db_column='traditional_food_image', blank=True, null=True)
    traditional_dress = models.TextField(db_column='traditional_dress', blank=True, null=True)
    traditional_dress_image = models.JSONField(db_column='traditional_dress_image', blank=True, null=True)
    traditional_ornaments = models.TextField(db_column='traditional_ornaments', blank=True, null=True)
    traditional_ornaments_image = models.JSONField(db_column='traditional_ornaments_image', blank=True, null=True)
    specific_rituals = models.TextField(db_column='specific_rituals', blank=True, null=True)
    festivals_name = models.TextField(db_column='festivals_name', blank=True, null=True)
    festivals_image = models.JSONField(db_column='festivals_image', blank=True, null=True)
    festival_participants = models.TextField(db_column='festival_participants', blank=True, null=True)
    festival_organizers = models.TextField(db_column='festival_organizers', blank=True, null=True)
    festival_special_dishes = models.TextField(db_column='festival_special_dishes', blank=True, null=True)
    art_forms_practiced = models.TextField(db_column='art_forms_practiced', blank=True, null=True)
    art_forms_practiced_image = models.JSONField(db_column='art_forms_practiced_image', blank=True, null=True)
    linked_to_rituals = models.TextField(db_column='linked_to_rituals', blank=True, null=True)
    # art_or_craft_form = models.TextField(db_column='art_or_craft_form', blank=True, null=True)
    production_techniques = models.TextField(db_column='production_techniques', blank=True, null=True)
    display_sale_occasions = models.TextField(db_column='display_sale_occasions', blank=True, null=True)
    stories_songs = models.TextField(db_column='stories_songs', blank=True, null=True)
    present_status_of_art = models.TextField(db_column='present_status_of_art', blank=True, null=True)
    suggestions_for_revitalization = models.TextField(db_column='suggestions_for_revitalization', blank=True, null=True)
    suggestions_for_self_reliant = models.TextField(db_column='suggestions_for_self_reliant', blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)
    created_at = models.DateTimeField(db_column='created_at', auto_now_add=True,db_index=True)

    user_id = models.ForeignKey(Register, db_column='user_id', on_delete=models.SET_NULL, related_name='village_cultural_profile', blank=True, null=True)

    class Meta:
        db_table = 'village_cultural_profile'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.village_id)