from django.urls import path
from myapps.event.views import EventSearchApi, event_detail_api, EventRegisterApi

from EventManager.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static

urlpatterns = [
    path('search/', EventSearchApi.as_view()),
    path('detail/', event_detail_api),
    path('register/', EventRegisterApi.as_view()),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
