#CODE: pasco-temperature-live.py
#Version: 20.10.2021
#Author: Vegard Rekaa, Pythonskole.no
#kontakt@pythonskole.no

# Documentation: https://pypi.org/project/pasco/
from pasco.pasco_ble_device import PASCOBLEDevice

from matplotlib import animation
import matplotlib.pyplot as plt
import time
import numpy as np #We only need polyfit here

device = PASCOBLEDevice()
available_devices = device.scan()
n = len(available_devices)
print("Found ",n," devices")
for dev in available_devices: 
    print(dev)
if n == 0: 
    print("Exiting")
    exit(0)

device_id = '508-699'
print("Connecting to my temperature sensor: ",device_id)
device.connect_by_id(device_id)

#print("Connecting to the first device in the list")
#print("Device: "+str(available_devices[0]))
#device.connect(available_devices[0])
if not device.is_connected():
    print("Connection failed")
    exit(0)

device.keepalive()

#set up the experiment
tid_start = time.time()
tid = 0
xmin = 0
xmax = 120.0
ymin = 10.0
ymax = 50.0
interval = 2000 #ms between each message
max_iterations = int((xmax-xmin)/(interval/1000))
data_type = 'Temperature'
xdata  = []
y1data = []
y2data = []


def curvefit():
    #Linear curve fit
    #if len(xdata) < 2:
    #    a,b = 0.0,0.0
    #else:
    #    a,b = np.polyfit(xdata,y1data,1)
    #return [a*x + b for x in xdata]
    #Fourth order polynomial curve fit
    if len(xdata) < 5:
        a,b,c,d,e = 0.0,0.0,0.0,0.0,0.0
    else:
        a,b,c,d,e = np.polyfit(xdata,y1data,4)
    return [a*x**4 + b*x**3 + c*x**2 + d*x + e for x in xdata]


#Set up figure, axis and plot element
fig = plt.figure()
ax  = plt.axes()
ax.set_xlim([xmin,xmax])
ax.set_ylim([ymin,ymax])
plt.xlabel("Tid (s)")
plt.ylabel("Temperatur (C)")
labels     = ['Data','Curve fit']
colors     = ["blue","red"]
linestyles = ['dotted','solid']
markers    = ['.','']

#Set up initial line elements
lines = []
for index in range(2):
    lobj = ax.plot([],[],linewidth=1,label=labels[index],color=colors[index],
            linestyle=linestyles[index],marker=markers[index])[0]
    lines.append(lobj)


# initialization function: plot the background
def init():
    for line in lines:
        line.set_data([],[])
    plt.legend()
    return lines

# animation function.  This is called sequentially
def animate(i):
    tid = time.time()-tid_start
    print("Frame:{0:3d} Tid:{1:6.2f}s  fps={2:4.1f}".\
            format(i,tid,i/tid),end='\r')
    xdata.append(tid)
    y1data.append(device.read_data(data_type))
    y2data = curvefit()
    lines[0].set_data(xdata,y1data)
    lines[1].set_data(xdata,y2data)
    return lines


# call the animator
print("Max iterations:",max_iterations)
anim = animation.FuncAnimation(fig, animate, init_func=init,
            frames=max_iterations, interval=interval, repeat=False)

#handles,labels = ax.get_legend_handles_labels()
#plt.legend(handles,labels)
plt.show()

device.disconnect()


