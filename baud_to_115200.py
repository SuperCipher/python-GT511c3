'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This is for to change the fingerprint baud rate 9600 to 115200,
The baudrate 9600 have troubles with response in usb serial devices

Executes this script only once
'''
import FPS, sys

DEVICE_GPIO = '/dev/ttyAMA0'
DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 9600 #initial baud rate
FPS.DEVICE_NAME = DEVICE_MAC

if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_MAC,is_com=True)
    fps.UseSerialDebug = True
    fps.ChangeBaudRate(115200)
    fps.Close()
    pass
