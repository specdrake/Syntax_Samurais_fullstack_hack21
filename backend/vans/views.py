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
    queryset = Waypoint.objects.all().order_by('eta')
    
    
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
        for ele in all[:4]:
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
        if Vaccination_Schedule.objects.filter(user=curr_user).exists():
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
        
class ListUser(generics.GenericAPIView):
    permission_classes = [AuthenticatedOfficer]
    serializer_class = ListAllSerializer
    
    def post(self,request):
        data = request.data
        waypoint_id = data.get('waypoint_id',None)
        date = data.get('date',None)
        if not waypoint_id:
            return Response({"status" : "Failed","errors" : "Waypoint id not provided"},status=status.HTTP_400_BAD_REQUEST)
        waypoint = Waypoint.objects.get(id=waypoint_id)
        res = []
        for ele in Vaccination_Schedule.objects.filter(waypoint=waypoint):
            if str(ele.date.date()) != date:
                continue
            curr_user = ele.user
            prof = Profile.objects.get(owner=curr_user)
            here = {
                'id' : curr_user.id,
                'name' : prof.name,
                'age' : prof.age,
                'aadhar' :  prof.aadhar,
                'phone' : prof.phone,
                'dose' : prof.received+1,
                'special' : prof.special
            }
            res.append(here)
        res.sort(key = lambda x : (x['special'],x['age']),reverse=True)
        return Response({"status" : "OK","result" : res},status=status.HTTP_200_OK)
    
class UserVaccinated(generics.GenericAPIView):
    permission_classes = [AuthenticatedOfficer]
    serializer_class = UserconfirmSerializer
    
    def post(self,request):
        data = request.data
        user_id = data.get('user_id',None)
        waypoint_id = data.get('waypoint_id',None)
        if not user_id:
            return Response({"status" : "Failed","errors" : "User id not provided"},status=status.HTTP_400_BAD_REQUEST)
        if not waypoint_id:
            return Response({"status" : "Failed","errors" : "Waypoint id not provided"},status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id = user_id)
        waypoint = Waypoint.objects.get(id=waypoint_id)
        if Vaccination_Schedule.objects.filter(user=user,waypoint=waypoint).exists():
            here = Vaccination_Schedule.objects.get(user=user,waypoint=waypoint)    
            here.delete()
            prof = Profile.objects.get(owner=user)
            prof.received += 1
            prof.save() 
            email_body = {
                'username' : user.username,
                'message' : 'You have been successfully administered a vaccine',
                'waypoint' : waypoint.name,
                'date' : timezone.now(),
                'brand' : here.van.brand,
                'dose' : here.type
            }
            data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Vaccine Confirmation','to_email' : user.email}
            Util.send_confirmation(data)
            return Response({"status" : "OK","result" :"Vaccine confirmation mail sent to user"},status=status.HTTP_200_OK)
        return Response({"status" : "Failed","result" :"No such Vaccine schedule exists"},status=status.HTTP_400_BAD_REQUEST)
    

class Sendgrievancemail(generics.GenericAPIView):
    permission_classes = [AuthenticatedOfficer]
    serializer_class = ListAllSerializer 
    
    def post(self,request):
        data = request.data
        waypoint_id = data.get('waypoint_id',None)
        date = data.get('date',None)
        if not waypoint_id:
            return Response({"status" : "Failed","errors" : "Waypoint id not provided"},status=status.HTTP_400_BAD_REQUEST)
        waypoint = Waypoint.objects.get(id=waypoint_id)
        for ele in Vaccination_Schedule.objects.filter(waypoint=waypoint):
            if str(ele.date.date()) == date:
                email_body = {
                    'username' : ele.user.username,
                    'message' : 'We regret to inform you that due to unavoidable circumstances your vaccination slot has been cancelled. We encourage you to book a new one',
                    'waypoint' : waypoint.name,
                    'date' : ele.date,
                    'brand' : ele.van.brand,
                    'dose' : ele.type
                }
                ele.delete()
                data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Slot Cancellation','to_email' : ele.user.email}
                Util.send_cancellation(data)
        return Response({"status" : "OK","result" : "All users assigned to this waypoint have been sent a cancellation email"})
    
class LocationMark(generics.GenericAPIView):
    permission_classes =[AuthenticatedOfficer]
    serializer_class = LocationMark
    
    def post(self,request):
        data = request.data
        van_id = data.get('van_id',None) 
        if not van_id:
            return Response({"status" : "Failed","errors" : "Van id not provided"},status=status.HTTP_400_BAD_REQUEST)
        curr_van = Van.objects.get(id=van_id)
        queue = Waypoint_Queue.objects.filter(van=curr_van).order_by('eta')
        temp = queue[0]
        queue[0].delete()
        cnt = Waypoint_Queue.objects.filter(van=curr_van).order_by('eta').count()
        if cnt == 0:
            return Response({"status" : "OK","result" : "Location Updated"},status=status.HTTP_200_OK)
        temp = queue[0].waypoint
        curr_van.latitude = temp.latitude
        curr_van.longitude = temp.longitude
        curr_van.save() 
        for ele in Vaccination_Schedule.objects.filter(waypoint=queue[0].waypoint):
            email_body = {
                'username' : ele.user.username,
                'message' : 'Your slot is next, Get ready at the given slot and time',
                'waypoint' : ele.waypoint.name,
                'date' : ele.date,
                'brand' : ele.van.brand,
                'dose' : ele.type
            } 
            data = {'email_body' : email_body,'email_subject' : 'LoCoWin - Slot Reminder','to_email' : ele.user.email}
            Util.send_confirmation(data)
        return Response({"status" : "OK","result" : "Van location updated and users in the next slot have been informed"},status=status.HTTP_200_OK)


class VanALLView(generics.ListAPIView):
    permission_classes =[AuthenticatedOfficer]
    serializer_class = VanSerialzier
    queryset = Van.objects.all()
    
class SpecificVan(generics.RetrieveAPIView):
    permission_classes = [AuthenticatedOfficer]
    serializer_class = VanSerialzier
    queryset = Van.objects.all()
    lookup_field = 'id'
    
