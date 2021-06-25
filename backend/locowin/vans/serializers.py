from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *
from user.models import *
from django.contrib import auth
from user.exception import *

class AllSlotsSerializer(serializers.ModelSerializer):
    van_info = serializers.SerializerMethodField()
    
    def get_van_info(self,attrs):
        queue = Waypoint_Queue.objects.get(waypoint=attrs)
        van_here = Van.objects.get(id=queue.van.id)
        res = {
            "dose1" : van_here.d1,
            "dose2" : van_here.d2,
            "brand" : van_here.brand,
        }
        return res
    
    
    class Meta:
        model = Waypoint
        fields = ('id','name','capacity','duration','latitude','longitude','eta','van_info')
