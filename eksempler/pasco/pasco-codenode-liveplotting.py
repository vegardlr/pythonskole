#LIVE PLOTTING WITH PASCO PYTHON MODULE
#CONTACT: kontakt@pythonskole.no
#Version 15.10.2021

# Documentation: https://pypi.org/project/pasco/
from pasco.pasco_ble_device import PASCOBLEDevice
from pasco.code_node_device import CodeNodeDevice
from pasco.character_library import Icons

from matplotlib import animation
import matplotlib.pyplot as plt
import time
import numpy as np


##############################################################
#Edit this section: 
##############################################################
# Say what data you want to plot from the code-node. 
# These are your options: 
# 'Temperature', 'Brightness', 'Loudness', 'MagneticFieldStrength', 
# 'Accelerationx', 'Accelerationy', 'TiltAngleX', 'TiltAngleY', 
# 'CartPosition', 'CartVelocity', 'Button1', 'Button2'
data    = 'Accelerationy'   #Choose from the list above
measure_time = 15.0         #Say how many seconds you want to measure
ymin =  -15                  #What max/min y-values do you expect
ymax =  15
max_iterations = 200        #At how many iterations do you wish to abort?
dump_data = True


#################################################################
################  EDIT THIS AT YOUR OWN RISK ####################
#################################################################


# Create a code element, through which we can handle the instrument
codenode = CodeNodeDevice()
# List all code.Node-devices
codenode_list = codenode.scan('//code.Node')
if codenode_list:  # Go forth if some devices are found
    # Print the list of devices
    for i, dev in enumerate(codenode_list):
        print(str(i)+":"+str(dev))
    # Get user input which device you want. 
    # If there is only one, select that device automatically
    select = input('Select a codenode: ') if len(codenode_list) > 1 else 0
    select_codenode = codenode_list[int(select)]
    print("Connecting to:"+str(select_codenode))
    codenode.connect(select_codenode)
else:
    print("No codenode found")
    exit(0)

if not codenode.is_connected():
    print("Connection failed")
    exit(0)

#Prevent the device to disconnect after 5 minutes
codenode.keepalive()

led_list = [[0,0],[1,1], [3,3], [2,2], [4,4]]
codenode.set_leds_in_array(led_list, 128)
time.sleep(1)
codenode.set_sound_frequency(440)
time.sleep(1)
led_list = [[0,4],[1,3], [2,2], [3,1], [4,0]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(0, 50, 150)
time.sleep(1)
led_list = [[0,0],[1,1], [3,3], [2,2], [4,4]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(150, 50, 0)
time.sleep(1)
led_list = [[0,4],[1,3], [2,2], [3,1], [4,0]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(150, 150, 50)
time.sleep(1)
led_list = [[0,0],[1,1], [3,3], [2,2], [4,4]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(0, 50, 150)
time.sleep(1)
led_list = [[0,4],[1,3], [2,2], [3,1], [4,0]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(150, 50, 0)
time.sleep(1)
led_list = [[0,0],[1,1], [3,3], [2,2], [4,4]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_rgb_led(150, 150, 50)
time.sleep(1)
led_list = [[0,4],[1,3], [2,2], [3,1], [4,0]]
codenode.set_leds_in_array(led_list, 128)
codenode.set_sound_frequency(0)
time.sleep(2)

#Setup data storage and plotting parameters
xdata   = []
ydata   = []
t_start = time.time()
t_stop  = t_start+measure_time
xdata_range = [0,measure_time]
ydata_range = [ymin,ymax]

#Set up figure, axis and plot element
fig = plt.figure()
ax  = plt.axes()
plt.title(data)
plt.ylabel(data)
plt.xlabel('Tid (s)')
ax.set_xlim(xdata_range)
ax.set_ylim(ydata_range)
line, = ax.plot([], [])

# initialization function: plot the background
def init():
    line.set_data([],[])
    return line,

# animation function.  This is called sequentially
def animate(i):
    tid = time.time()-t_start
    verdi = codenode.read_data(data)
    xdata.append(tid)
    ydata.append(verdi)
    line.set_data(xdata,ydata)
    if dump_data: 
        print("Frame:{0:3d} Tid:{1:6.2f}s  fps={2:4.1f}  "+data+"={3:10.4f}".\
            format(i,tid,i/tid,verdi),end='\r')
    else: 
        print("Frame:{0:3d} Tid:{1:6.2f}s  fps={2:4.1f}".\
                format(i,tid,i/tid),end='\r')
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
            frames=max_iterations, interval=1, blit=True, repeat=False)
plt.show()



# My experience is that this is needed to avoid 
# bluetooth-issues at connection-time
codenode.disconnect()


