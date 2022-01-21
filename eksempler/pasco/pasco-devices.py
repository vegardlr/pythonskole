# pasco-device.py
# Looks for Pasco devices and prints their available 
# sensors and measurments. Then disconnects.
# Written by Vegard Rekaa 2021, kontakt@pythonskole.no
# 
# Import pasco libraries
# Documentation: https://pypi.org/project/pasco/
from sys import exit
from pasco.pasco_ble_device import PASCOBLEDevice
from pasco.code_node_device import CodeNodeDevice
from pasco.character_library import Icons

# Create handle to manage devices
device = PASCOBLEDevice()

# Read available bluetooth devics. 
# Please make sure of the following 
# before running this code: 
#  - the PC's bluetooth is on
#  - the device(s) is on and blinking red (not green)
#  - the device(s) are close to the PC
found_devices = device.scan()
n = len(found_devices)
print("Found ",n," devices")
if n == 0: exit(0)  #Exit code if no devices are found

#Print list of available devices
for i, ble_device in enumerate(found_devices):
    print(f'{i}: {ble_device.name}')

#Ask for user input, for what device we want to analyze
selected_device = found_devices[int(input('Select a device: '))]

#Connect to device
print("Connecting to:"+str(selected_device))
device.connect(selected_device)

#Print warning if connection failed, exit code if fail
if not device.is_connected():
    print("Connection failed")
    exit(0)

#Print list of sensors on device
print("Sensor list:", device.get_sensor_list())
#Print list of measurments available with the sensors
print("Measurement list:", device.get_measurement_list())

#Clean disconnect. If the code exists with an error between 
#device.connect() and device.disconnect(), the devices will blink
#green after running this code. To make them available 
#for a new connection, you need to first turn them off, then 
#restart them (you want a red blinking light) on the bluetooth-lamp
device.disconnect()

