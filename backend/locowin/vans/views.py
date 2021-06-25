from rest_framework import generics,status,permissions,views
from user.permissions import *
from user.models import *
from .models import *
from rest_framework.response import Response
import datetime
from django.utils import timezone
from .serializers import *
from user.utils import Util


class Dashboard(generics.GenericAPIView):
    permission_classes = [Authenticated]
    
    def get(self,request):
        user = self.request.user
        here = Profile.objects.get(owner=user)
        res = {
            'status' : "OK",
            'doses' : here.received,
            "due_days" : None,
            "waypoint" : None,
            "datetime" : None,
            "message" : None,
        }
        if here.received == 2:
            res["message"] = "You have taken both the doses"
            return Response(res,status=status.HTTP_200_OK)
        check = Vaccination_Schedule.objects.filter(user=user,type=here.received+1)
        if check.exists():
            check = Vaccination_Schedule.objects.get(user=user)
            now = timezone.now()
            delta = check.date - now
            res["due_days"] = delta.days
            res["waypoint"]  = check.waypoint.name
            res["datetime"] = check.date
        else:
            res["message"] = "You are yet to book a slot for your next dose"
        return Response(res,status=status.HTTP_200_OK)