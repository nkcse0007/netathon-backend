from django.db import models
from utils.constants import *
from myapps.authentication.models import UserLoginInfo, CategoryModel, ArtistModel
from utils.db.base_model import AbstractBaseModel
from utils.services.zoom import createMeeting

class EventModel(AbstractBaseModel):
    organization = models.ForeignKey(UserLoginInfo, blank=False, on_delete=models.CASCADE)
    artists = models.ManyToManyField(ArtistModel)
    title = models.CharField(max_length=255, blank=True)
    category = models.ManyToManyField(CategoryModel)
    intro = models.TextField(blank=True)
    grid_image = models.ImageField(blank=True, null=True)
    banner = models.ImageField(blank=True, null=True)
    city = models.CharField(max_length=30, choices=CITIES)
    location = models.CharField(max_length=30, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()
    regular_price = models.PositiveIntegerField(blank=True, null=True)
    sale_price = models.PositiveIntegerField(blank=True, null=True)
    meeting_url = models.URLField(blank=True, null=True)
    meeting_password = models.CharField(max_length=50, blank=True, null=True)
    booking_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = "event_model"
        verbose_name = "Event Info"
        verbose_name_plural = "Event Information"

class EventRegistrationModel(AbstractBaseModel):
    user = models.ForeignKey(UserLoginInfo, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.event)

    class Meta:
        db_table = "event_registration_model"
        verbose_name = "Event Registration Info"
        verbose_name_plural = "Event Registration Information"