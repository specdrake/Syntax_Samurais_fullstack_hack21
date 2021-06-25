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
    
class AllSlots(generics.ListAPIView):
    serializer_class = AllSlotsSerializer
    queryset = Waypoint.objects.all()
    
    
class BestSlots(generics.GenericAPIView):
    permission_classes = [Authenticated]
    
    def get(self,request):
        user = self.request.user
        prof =  Profile.objects.get(owner=user)
        need_dose = prof.received+1
        lat = prof.latitude
        long = prof.longitude
        if need_dose == 3:
            return Response({"status" : "Failed","errors" : "You have already taken both the doses"},status=status.HTTP_400_BAD_REQUEST)
        all = []
        for ele in Waypoint.objects.all():
            queue = Waypoint_Queue.objects.get(waypoint=ele)
            van_here = Van.objects.get(id=queue.van.id)
            delta = ele.eta - timezone.now()
            if need_dose == 1:
                if van_here.d1 > 0 and ele.capacity > 0 and delta.seconds > 0:
                    all.append(ele)
            if need_dose == 2:
                if van_here.d2 > 0 and ele.capacity > 0 and delta.seconds > 0:
                    all.append(ele)
        all.sort(key = lambda x : abs(x.latitude-lat) + abs(x.longitude-long))
        print(all)
        res = []
        for ele in all[:5]:
            res.append(AllSlotsSerializer(ele).data)
        return Response({"status" : "OK","result" : res},status=status.HTTP_200_OK)