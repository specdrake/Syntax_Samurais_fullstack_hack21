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
            "id"    : van_here.id,
            "dose1" : van_here.d1,
            "dose2" : van_here.d2,
            "brand" : van_here.brand,
        }
        return res
    class Meta:
        model = Waypoint
        fields = ('id','name','capacity','latitude','longitude','eta','van_info')
    
class BookSlotSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    class Meta:
        fields = ('id','date') 
    class Meta:
        model = Waypoint
        fields = ('id','name','capacity','duration','latitude','longitude','eta','van_info')

class ListAllSerializer(serializers.Serializer):
    waypoint_id = serializers.IntegerField(required=True)
    date = serializers.DateField(required=True)
    class Meta:
        fields = ('waypoint_id','date',)

class UserconfirmSerializer(serializers.Serializer):
    waypoint_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    class Meta:
        fields = ('user_id','waypoint_id',)
        
class LocationMark(serializers.Serializer):
    van_id = serializers.IntegerField(required=True)
    
    class Meta:
        fields = ('van_id')
        
class VanSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Van
        fields = ('id','d1','d2','brand','latitude','longitude')
