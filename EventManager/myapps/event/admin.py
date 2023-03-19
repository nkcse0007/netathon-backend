from django.contrib import admin
from myapps.event.models import *


class EventAdmin(admin.ModelAdmin):
  list_display = ("title", "created_at")
  list_filter = ('category', 'artists', 'city', 'created_at')
  search_fields = ['title', 'city', 'location']

  fieldsets = (
    ('Basic Information', {
      'fields': ('organization', 'title', 'intro', 'banner', 'grid_image')
    }),
    ('Location', {
      'classes': ('wide',),
      'fields': ('city','location'),
    }),
    ('Details', {
      'classes': ('wide',),
      'fields': ('artists', 'category'),
    }),
    ('Other', {
      'classes': ('wide',),
      'fields': ('booking_count', 'event_date', 'regular_price','sale_price', 'meeting_url', 'meeting_password'),
    }),
    )
  filter_horizontal = ('category', 'artists')

  def _generate_meeting_details(self, obj):
        return {
          "topic": obj.title,
          "type": 2,
          "start_time": str(obj.event_date),
          "duration": "45",
          "timezone": "Asia/Kolkata",
          "agenda": obj.intro,

          "recurrence": {"type": 1,
                          "repeat_interval": 1
                          },
          "settings": {"host_video": "true",
                      "participant_video": "true",
                      "join_before_host": "true",
                      "mute_upon_entry": "False",
                      "watermark": "true",
                      "audio": "voip",
                      "auto_recording": "cloud"
                      }
          }
  
  def save_model(self, request, obj, form, change):
    if not change:
      url, password = createMeeting(self._generate_meeting_details(obj))
      obj.meeting_url = url
      obj.meeting_password = password
    super().save_model(request, obj, form, change)
  
  def get_queryset(self, request):
    queryset = super(EventAdmin, self).get_queryset(request)
    if request.user.role == ORGANIZATION_ROLE_TYPE:
      queryset= queryset.filter(organization=request.user)
    return queryset

admin.site.register(EventModel, EventAdmin)
admin.site.register(EventRegistrationModel)