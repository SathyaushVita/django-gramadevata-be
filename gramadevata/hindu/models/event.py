

from enum import Enum
import uuid
from datetime import datetime

from django.db import models
from django.utils import timezone

from ..enums import EventTag, GeoSite, EntityStatus
from .event_category import EventCategory
from .register import Register
from .village import Village
from .temple import Temple
from ..enums import ActivityOption, EntityStatus
from .country import Country

class EventStatusEnum(Enum):
    UPCOMING = "Upcoming"
    COMPLETED = "Completed"
    ONGOING = "Ongoing"


class Event(models.Model):
    _id = models.CharField(db_column='_id', primary_key=True, max_length=45, default=uuid.uuid1, unique=True, editable=False,db_index=True)
    category = models.ForeignKey(EventCategory, db_column='category', on_delete=models.SET_NULL, null=True, blank=True,db_index=True)
    name = models.CharField(db_column='name', max_length=45, null=True, blank=True,db_index=True)

    start_date = models.DateField(db_column='start_date', null=True, blank=True)
    end_date = models.DateField(db_column='end_date', null=True, blank=True)
    start_time = models.TimeField(db_column='start_time', null=True, blank=True)
    end_time = models.TimeField(db_column='end_time', null=True, blank=True)

    tag = models.CharField(db_column='tag', max_length=50, choices=[(e.name, e.value) for e in EventTag], default=None, blank=True, null=True)
    tag_id = models.CharField(null=True, max_length=45)
    tag_type_id = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)

    geo_site = models.CharField(max_length=50, choices=[(e.name, e.value) for e in GeoSite], default=GeoSite.VILLAGE.value,db_index=True)
    object_id = models.ForeignKey(Village, db_column='object_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='events',db_index=True)
    content_type_id = models.IntegerField(null=True, blank=True)

    map_location = models.URLField(db_column='map_location', max_length=450, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=200, blank=True, null=True)

    contact_name = models.CharField(db_column='contact_name', max_length=45, blank=True, null=True)
    contact_phone = models.CharField(db_column='contact_phone', max_length=10, blank=True, null=True)
    contact_email = models.CharField(db_column='contact_email', max_length=45, blank=True, null=True)

    desc = models.TextField(db_column='desc', blank=True, null=True)
    status = models.CharField(db_column='status', max_length=50, choices=[(e.name, e.value) for e in EntityStatus], default=EntityStatus.INACTIVE.value,db_index=True)

    user = models.ForeignKey(Register, db_column='user_id', on_delete=models.SET_NULL, related_name='events', null=True)
    image_location = models.JSONField(db_column='image_location', blank=True, null=True, default=list)
    temple = models.ForeignKey(Temple, db_column='temple_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='events',db_index=True)

    event_status = models.CharField(db_column='event_status', max_length=50, choices=[(e.name, e.value) for e in EventStatusEnum], default=EventStatusEnum.UPCOMING.name)
    event_video = models.JSONField(db_column='event_video', null=True, blank=True, default=list)  
    organized_by= models.CharField(db_column='organized_by',max_length=100, null=True, blank=True,)
    food = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    water = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    toilets = models.CharField(max_length=20, choices=[(e.name, e.value) for e in ActivityOption], default=ActivityOption.NO.value)
    country_name=models.CharField(db_column='country_name', max_length=100, blank=True, null=True,db_index=True)
    state_name=models.CharField(db_column='state_name', max_length=100, blank=True, null=True,db_index=True)
    district_name=models.CharField(db_column='district_name', max_length=100, blank=True, null=True,db_index=True)
    block_name=models.CharField(db_column='block_name', max_length=100, blank=True, null=True,db_index=True)
    village_name=models.CharField(db_column='village_name', max_length=100, blank=True, null=True,db_index=True)
    other_name=models.CharField(db_column='other_name', max_length=100, blank=True, null=True,db_index=True)
    country = models.ForeignKey(Country,related_name="events",on_delete=models.CASCADE,blank=True, null=True,db_index=True,db_column="country")




    @property
    def relative_time(self):
        if not self.start_date or not self.start_time:
            return "Unknown"
        try:
            start_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
        except ValueError as e:
            return f"Invalid date or time format: {e}"
        
        now = timezone.now()

        if start_datetime > now:
            diff = start_datetime - now
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes to go"
            elif diff.days == 1:
                return "1 day to go"
            else:
                return f"{diff.days} days to go"
        else:
            diff = now - start_datetime
            if diff.days == 0:
                hours, remainder = divmod(diff.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{hours} hours, {minutes} minutes ago"
            elif diff.days == 1:
                return "1 day ago"
            else:
                return f"{diff.days} days ago"

    # def update_event_status(self):
    #     now = timezone.now()
    #     if self.start_date and self.start_time and self.end_date and self.end_time:
    #         try:
    #             start_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
    #             end_datetime = timezone.make_aware(datetime.combine(self.end_date, self.end_time))

    #             if now < start_datetime:
    #                 self.event_status = EventStatusEnum.UPCOMING.name
    #             elif start_datetime <= now <= end_datetime:
    #                 self.event_status = EventStatusEnum.ONGOING.name
    #             else:
    #                 self.event_status = EventStatusEnum.COMPLETED.name

    #             self.save()
    #         except ValueError as e:
    #             print(f"Error updating event status: {e}")


    def update_event_status(self):
        now = timezone.now()

        if self.start_date and self.start_time and self.end_date and self.end_time:
            try:
                # Combine date and time
                start_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
                end_datetime = timezone.make_aware(datetime.combine(self.end_date, self.end_time))

                # Compare with current time
                if now < start_datetime:
                    self.event_status = EventStatusEnum.UPCOMING.name
                elif start_datetime <= now <= end_datetime:
                    self.event_status = EventStatusEnum.ONGOING.name
                else:
                    self.event_status = EventStatusEnum.COMPLETED.name

                self.save()
            except Exception as e:
                print(f"Error updating event status: {e}")



    class Meta:
        managed = True
        db_table = 'event'
