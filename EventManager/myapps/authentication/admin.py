from django.contrib import admin
from django.contrib.auth.hashers import make_password
from myapps.authentication.models import *

from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
  list_display = ("name", "email", "role", "created_at")
  list_filter = ('role', 'created_at', 'is_active', 'is_deleted')
  search_fields = ['name', 'email', 'role']
  
  fieldsets = (
    ('Basic Information', {
        'fields': ('name', 'email', 'password', 'phone_code', 'phone')
    }),
    ('Details', {
        'classes': ('wide',),
        'fields': ('role', 'profile_summary'),
    }),
    ('Configurations', {
        'classes': ('wide',),
        'fields': ('is_verified','is_deleted','is_active'),
    }),
    )

  def save_model(self, request, obj, form, change):
    if not change and obj.role == ORGANIZATION_ROLE_TYPE:
        obj.is_staff=True
        obj.password = make_password(obj.password)
    super().save_model(request, obj, form, change)

admin.site.register(UserLoginInfo, UserAdmin)

class ArtistAdmin(admin.ModelAdmin):
  list_filter = ('category',)
  search_fields = ['title', 'user__name', 'category']
  filter_horizontal = ('category',)
admin.site.register(ArtistModel, ArtistAdmin)

admin.site.register(OrganizationModel)
admin.site.register(CategoryModel)

admin.site.unregister(Group)