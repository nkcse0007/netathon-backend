from django.contrib import admin
from django.urls import path, include
from EventManager.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from myapps.event.views import GetDataApi

urlpatterns = [
                  path('api/admin/', admin.site.urls),
                  path('api/master/', GetDataApi),
                  path('api/auth/', include('myapps.authentication.urls'), name='authentication'),
                  path('api/event/', include('myapps.event.urls'), name='event'),
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
