import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locowin.settings")
django.setup()

from user.models import User
from vans.models import Waypoint, Van, Waypoint_Queue
import subprocess
from random import choice
import datetime
import pytz 

# global variables
capacity = 200
d1 = 150
d2 = 50
brands = ["Covishield", "Covaxin", "Sputnik"]
numVans = 10
numWp= 50
init_lat = 77.0
init_lon = 28.0
num_wp = 5
duration = 2 # hours
intz= pytz.timezone("Asia/Kolkata")
init_time = datetime.datetime(2021, 6, 28, 8, 0, 0, 0)
init_time = intz.localize(init_time)


def compile():
    data = subprocess.Popen(['g++', '-o', 'data_points/generator', 'data_points/generator.cpp', 'data_points/helpers/calc.cpp'], stdout=subprocess.PIPE)
    output = data.communicate()
    print(output)
    data2 = subprocess.Popen(['g++', '-o', 'data_points/hotspot_kmc', 'data_points/hotspot_kmc.cpp', 'data_points/helpers/calc.cpp'], stdout=subprocess.PIPE)
    output2 = data2.communicate()
    print(output2)
    data3 = subprocess.Popen(['g++', '-o', 'data_points/ant_routing', 'data_points/ant_routing.cpp', 'data_points/helpers/calc.cpp'], stdout=subprocess.PIPE)
    output3 = data3.communicate()
    print(output3)
    # running

def generate(seed):
    print("starting bash script")
    strseed = str(seed)
    data4 = subprocess.Popen(['./scr.bash', strseed], stdout=subprocess.PIPE)
    output4 = data4.communicate()
    print(output4)
    print("done")

def makeWaypoints(vanpath):
    fl = open(vanpath, "r")
    content = fl.read()
    fl.close()
    lines = content.splitlines()
    print(len(lines))
    for i in range(1,len(lines)):
        lon, lat = lines[i].split()
        Waypoint.objects.create(capacity=capacity, name="waypoint"+str(i), latitude=float(lat), longitude=float(lon))
        print(i, "-->", lon, lat)

def makeVans():
   for i in range(numVans):
       Van.objects.create(d1=d1, d2=d2, brand=choice(brands), latitude=init_lat, longitude=init_lon)

def makeWpQueue():
    print()
    offsetw = Waypoint.objects.order_by('id')[0].id
    offsetv = Van.objects.order_by('id')[0].id
    for i in range(numWp):
        van = i / 5 + offsetv;
        eta = init_time + datetime.timedelta(hours=(i % 5) * duration)
        print(i + 1,"--> ", eta)
        wpoint = Waypoint.objects.get(id=i+offsetw)
        Waypoint_Queue.objects.create(waypoint=wpoint, van=Van.objects.get(id=van), eta=eta)
        wpoint.eta = eta
        wpoint.save()

if __name__=='__main__':
    #compile()
    #generate(3)

    makeWaypoints('./data_points/van_path')
    makeVans()
    makeWpQueue()
