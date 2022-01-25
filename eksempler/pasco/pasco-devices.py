# pasco-device.py
# Looks for Pasco devices and prints their available 
# sensors and measurments. Then disconnects.
# Written by Vegard Rekaa 2021, kontakt@pythonskole.no
# Updated January 2022
# 
# Documentation on pasco libraries: https://pypi.org/project/pasco/
from sys import exit
from pasco.pasco_ble_device import PASCOBLEDevice
#from pasco.code_node_device import CodeNodeDevice
#from pasco.character_library import Icons

# Create a code element, through which we can handle the instrument
device = PASCOBLEDevice()
# List all devices
device_list = device.scan()
if len(device_list) == 0:
    #Leace program if no devices are found
    print("No device found")
    exit(0)

# Print the list of devices
for i, dev in enumerate(device_list):
    print(str(i)+":"+str(dev))
# Get user input which device you want. 
# If there is only one, select that device automatically
select = input('Select a device: ') if len(device_list) > 1 else 0
select_device = device_list[int(select)]
#Print the name and ID of the selected device, and connect
print("Connecting to:"+str(select_device))
device.connect(select_device)

#Leave code if connection failed
if not device.is_connected():
    print("Connection failed")
    exit(0)

#Print list of sensors on connected device
print("Sensor list:", device.get_sensor_list())
#Print list of measurments available from the connected device
print("Measurement list:", device.get_measurement_list())

#Clean disconnect. 
device.disconnect()

