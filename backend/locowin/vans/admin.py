from django.contrib import admin
from .models import Waypoint,Waypoint_Queue,Van,Vaccination_Officer,Vaccination_Schedule
# Register your models here.

admin.site.register(Waypoint)
admin.site.register(Vaccination_Schedule)
admin.site.register(Vaccination_Officer)
admin.site.register(Waypoint_Queue)
admin.site.register(Van)
