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
    

class BookSlot(generics.GenericAPIView):
    permission_classes = [Authenticated]
    serializer_class = BookSlotSerializer
    
    def post(self, request):
        data = request.data
        user = self.request.user
        curr_user = User.objects.get(username=user)
        prof =  Profile.objects.get(owner=user)
        need_dose = prof.received+1   
        id_here = data.get('id',None)
        date = data.get('date',None)
        if not id_here:
            return Response({"status" : "Failed","errors" : "Waypoint id required for booking a slot"},status=status.HTTP_400_BAD_REQUEST)
        if not Waypoint.objects.filter(id=id_here).exists():
            return Response({"status" : "Failed","errors" : "No such Waypoint exists"},status=status.HTTP_400_BAD_REQUEST)
        waypoint = Waypoint.objects.get(id=id_here)
        cnt = 0
        for ele in Vaccination_Schedule.objects.filter(waypoint=waypoint):
            if str(ele.date.date()) == date:
                cnt += 1
        if cnt >= waypoint.capacity:
            return Response({"status" : "Failed","errors" : "Waypoint is fully booked"},status=status.HTTP_400_BAD_REQUEST)
        delta = waypoint.eta - timezone.now()
        if delta.seconds <= 0:
            return Response({"status" : "Failed","errors" : "Waypoint is fully booked"},status=status.HTTP_400_BAD_REQUEST)
        if Vaccination_Schedule.objects.filter(waypoint=waypoint,user=curr_user).exists():
            return Response({"status" : "Failed","errors" : "You already have one booked slot"},status=status.HTTP_400_BAD_REQUEST)
        queue = Waypoint_Queue.objects.get(waypoint=waypoint)
        van_here = Van.objects.get(id=queue.van.id)
        if need_dose == 1:
            if van_here.d1 == 0:
               return Response({"status" : "Failed","errors" : "Dose 1 fully booked at this waypoint"},status=status.HTTP_400_BAD_REQUEST) 
            waypoint.capacity -= 1
            waypoint.save()
            van_here.d1 -= 1
            van_here.save()
            Vaccination_Schedule.objects.create(
                van = van_here,
                user = curr_user,
                date = waypoint.eta,
                waypoint = waypoint,
                brand = van_here.brand,
                type = need_dose
            )
            email_body = {
                'username' : user.username,
                'message' : 'Your vaccine slot has been booked with the following information',
                'waypoint' : waypoint.name,
                'date' : waypoint.eta,
                'brand' : van_here.brand,
                'dose' : 1
            }
            data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Slot Confirmation','to_email' : user.email}
            Util.slot_send_email(data)
            return Response({"status" : "OK","result" : "The given slot has been booked and a confirmation mail has been sent"},status=status.HTTP_200_OK)
        elif need_dose == 2:
            if van_here.d2 == 0:
                   return Response({"status" : "Failed","errors" : "Dose 2 fully booked at this waypoint"},status=status.HTTP_400_BAD_REQUEST) 
            waypoint.capacity -= 1
            waypoint.save()
            van_here.d2 -= 1
            van_here.save()
            Vaccination_Schedule.objects.create(
                van = van_here,
                user = curr_user,
                date = waypoint.eta,
                waypoint = waypoint,
                brand = van_here.brand,
                type = need_dose
            )
            email_body = {
                'username' : user.username,
                'message' : 'Your vaccine slot has been booked with the following information',
                'waypoint' : waypoint.name,
                'date' : waypoint.eta,
                'brand' : van_here.brand,
                'dose' : 2
            }
            data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Slot Confirmation','to_email' : user.email}
            Util.slot_send_email(data)
            return Response({"status" : "OK","result" : "The given slot has been booked and a confirmation mail has been sent"},status=status.HTTP_200_OK)
        else:
            return Response({"status" : "Failed","errors" : "You have already taken both the doses"},status=status.HTTP_400_BAD_REQUEST)