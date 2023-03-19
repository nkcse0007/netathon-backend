from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from myapps.authentication.managers.user import ManagerAccountUser
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from utils.constants import *
from utils.db.base_model import AbstractBaseModel
import re


class UserLoginInfo(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    role = models.CharField(max_length=15, choices=ROLE_TYPE, default=USER_ROLE_TYPE, blank=False, null=False,
                            help_text='Type of role.')
    name=models.CharField(max_length=255, blank=True)
    profile_summary=models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    password = models.TextField(blank=False, null=False)
    phone = models.CharField(max_length=10, default='', blank=True)
    phone_code = models.CharField(max_length=14, default='', blank=True)
    is_verified = models.BooleanField(default=False, help_text="Toggles verification status for a user.")
    is_deleted = models.BooleanField(default=False, help_text="Toggles soft delete status for a user.")
    is_active = models.BooleanField(default=True, help_text="Toggles active status for a user.")
    created_at = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False,
                                   help_text="Designates the user as "
                                             "a staff member.")

    is_superuser = models.BooleanField(default=False,
                                       help_text="Designates the user as"
                                                 " a super user.")

    objects = ManagerAccountUser()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user_login_info_model"
        verbose_name = "User"
        verbose_name_plural = "User Login Information"

    def __str__(self):
        return str(self.email)

    def auto_login(self, request):
        self.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, self)

    def save(self, *args, **kwargs):
        from myapps.event.models import EventModel, EventRegistrationModel
        organization_group, created = Group.objects.get_or_create(name=ORGANIZATION_ROLE_TYPE)
        if self.role == ORGANIZATION_ROLE_TYPE:
            if created:
                event_content_type = ContentType.objects.get_for_model(EventModel)
                organization_event_permission = Permission.objects.filter(content_type=event_content_type)
                for perm in organization_event_permission:
                    organization_group.permissions.add(perm)
                registeration_content_type = ContentType.objects.get_for_model(EventRegistrationModel)
                organization_register_permission = Permission.objects.filter(content_type=registeration_content_type)
                for perm in organization_register_permission:
                    organization_group.permissions.add(perm)
                
        super(UserLoginInfo, self).save(*args, **kwargs)
        person = UserLoginInfo.objects.get(id=self.id)
        person.groups.add(organization_group)


class OrganizationModel(AbstractBaseModel):
    user = models.OneToOneField(UserLoginInfo, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False)
    images = models.ImageField(blank=True, null=True)
    address = models.CharField(max_length=30, default='', blank=True)
    city = models.CharField(max_length=30, default='', blank=True)
    regular_price = models.PositiveIntegerField(null=True)
    sale_price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "organization_model"
        verbose_name = "Organization Info"
        verbose_name_plural = "Organization Information"


class CategoryModel(AbstractBaseModel):
    title = models.CharField(max_length=255)
    about = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "category_model"
        verbose_name = "Category_Info"
        verbose_name_plural = "Category Information"


class ArtistModel(AbstractBaseModel):
    user = models.OneToOneField(UserLoginInfo, blank=False, on_delete=models.CASCADE)
    images = models.ImageField(blank=True, null=True)
    location = models.CharField(max_length=30, default='', blank=True)
    city = models.CharField(max_length=30, default='', blank=True)
    category = models.ManyToManyField(CategoryModel)
    fees = models.PositiveIntegerField(default=0, null=True)
    working_since = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        db_table = "artist_model"
        verbose_name = "Artist_Info"
        verbose_name_plural = "Artist Information"
