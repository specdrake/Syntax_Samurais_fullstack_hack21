from django.db import models
from user.models import User

class Waypoint(models.Model):
    capacity = models.IntegerField(null=True,blank=True)
    latitude = models.DecimalField(max_digits = 15,decimal_places=9,null=True,blank=True)
    longitude = models.DecimalField(max_digits = 15,decimal_places=9,null=True,blank=True)
    eta = models.DateTimeField(null = True,blank=True)
    name = models.CharField(max_length=200, null=True,blank=True)
    
    def __str__(self):
        return self.name
    
class Van(models.Model):
    d1 = models.IntegerField(null=True,blank=True)
    d2 = models.IntegerField(null=True,blank=True)
    brand = models.CharField(max_length=200, null=True,blank=True)
    latitude = models.DecimalField(max_digits = 15,decimal_places=9,null=True,blank=True)
    longitude = models.DecimalField(max_digits = 15,decimal_places=9,null=True,blank=True)
    
    def __str__(self):
        return "Van " + str(self.id)
class Vaccination_Officer(models.Model):
    van = models.ForeignKey(to=Van,on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    
class Waypoint_Queue(models.Model):
    waypoint = models.ForeignKey(to=Waypoint,on_delete=models.CASCADE)
    van = models.ForeignKey(to=Van,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.waypoint.name + "--> Van " + str(self.van.id)
    
class Vaccination_Schedule(models.Model):
    van = models.ForeignKey(to=Van,on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    date = models.DateTimeField(null=True,blank=True)   
    waypoint = models.ForeignKey(to=Waypoint,on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, null=True,blank=True)
    type = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user.username) + "'s Dose " + str(self.type)