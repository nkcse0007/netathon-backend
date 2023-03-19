from django.contrib import admin
from myapps.authentication import admin
from myapps.event import admin

from django.contrib import admin as django_admin
django_admin.site.site_header = 'Booking bee'
django_admin.site.index_title = 'Booking bee'
