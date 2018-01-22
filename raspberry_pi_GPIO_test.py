'''
Created on 08/04/2014

@author: jeanmachuca

SAMPLE CODE:

This script is a test for device connected to GPIO port in raspberry pi

For test purpose:

Step 1:
Connect the TX pin of the fingerprint GT511C3 to RX in the GPIO

Step 2:
Connect the RX pin of the fingerprint GT511C3 to TX in the GPIO

Step 3:
Connect the VCC pin of the fingerprint GTC511C3 to VCC 3,3 in GPIO

Step 4:
Connect the Ground pin of fingerprint GT511C3 to ground pin in GPIO


This may be works fine, if don't, try to change the fingerprint baud rate with baud_to_115200.py sample code

modified by Napat Charuphant <napat_pat3@hotmail.com> on october 2017

'''
from socketIO_client import SocketIO
import RPi.GPIO as GPIO #for external led
import time #for external led
import FPS, sys
DEVICE_GPIO = '/dev/ttyAMA0'
# DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
# DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
# DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 9600
FPS.DEVICE_NAME = DEVICE_GPIO
socket_cmd = 'string'
socket_data = 1

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_fps_com_response(*args):
    # print(type(args))
    x = args[0]
    print(x['msg'])
    # print x
    global socket_cmd
    socket_cmd = x['msg']
    global socket_data
    socket_data = x['data']
    # print socket_data


# socketIO = SocketIO('http://192.168.1.40', 8080, verify=False)
# socketIO = SocketIO('http://192.168.2.1', 8080, verify=False)
socketIO = SocketIO('localhost', 8080, verify=False)
socketIO.on('connect', on_connect)
socketIO.on('fps_com', on_fps_com_response)
socketIO.emit('fps_com', {'msg':'FPS >>> standby'})
socketIO.wait(0.5)

def waitUntilPress(fps):
    while fps.IsPressFinger() == False:
        FPS.delay(FPS.INTERVAL+0.03)

def waitUntilRelease(fps):
    while fps.IsPressFinger() == True:
        FPS.delay(FPS.INTERVAL+0.03)

def identifyprotocol(fps):
    waitUntilPress(fps)
    if fps.CaptureFinger(True):
        return fps.Identify1_N()
    else:
        return 'Fail to identify'

def printEnroll():
    enrollid=0
    okid=True
    #search for a free enrollid, you have max 200
    while enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print okid
        enrollid+=1

def LegacyEnroll(fps):
    '''
    Enroll test
    '''
    fps.SetLED(False) # Turns OFF the CMOS LED
    enrollid=0
    okid=True
    msg='string'
    #search for a free enrollid, you have max 200
    while okid == True and enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print okid
        if okid == True:
            enrollid+=1
    fps.SetLED(True) # Turns ON the CMOS LED
    if enrollid <200:
        #press finger to Enroll enrollid
        # print 'Press finger to Enroll %s' % str(enrollid)'
        msgReal = 'Press finger to Enroll ID: %s' % str(enrollid)
        msg = {'msg':msgReal}
        socketIO.emit('fps_com', msg)
        fps.EnrollStart(enrollid)
        waitUntilPress(fps)
        iret = 0
        if fps.CaptureFinger(True):
            #remove finger
            # print 'remove finger'
            msg = {'msg':'remove finger'}
            socketIO.emit('fps_com', msg)
            fps.Enroll1()
            waitUntilRelease(fps)
            #Press same finger again
            # print 'Press same finger again'
            msg = {'msg':'Press finger for the second time'}
            socketIO.emit('fps_com', msg)
            waitUntilPress(fps)
            if fps.CaptureFinger(True):
                #remove finger
                # print 'remove finger'
                msg = {'msg':'remove finger'}
                socketIO.emit('fps_com', msg)
                fps.Enroll2()
                waitUntilRelease(fps)
                #Press same finger again
                # print 'press same finger yet again'
                msg = {'msg':'final press'}
                socketIO.emit('fps_com', msg)
                waitUntilPress(fps)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    if iret == 0:
                        # print 'Enrolling Successfull'
                        msg = {'msg':'Enrolled Successfull','data':enrollid}
                        socketIO.emit('fps_com', msg)
                    else:
                        # print 'Enrolling Failed with error code: %s' % str(iret)
                        if(iret == 3):
                            msg = {'msg':'Failed : Found duplicate finger'}
                            socketIO.emit('fps_com', msg)
                        else:
                            msgReal = 'Failed with error code: %s' % str(iret)
                            msg = {'msg':msgReal}
                            socketIO.emit('fps_com', msg)
                else:
                    # print 'Failed to capture third finger'
                    msg = {'msg':'Failed to capture third finger'}
                    socketIO.emit('fps_com', msg)
            else:
                # print 'Failed to capture second finger'
                msg = {'msg':'Failed to capture second finger'}
                socketIO.emit('fps_com', msg)
        else:
            # print 'Failed to capture first finger'
            msg = {'msg':'Failed to capture first finger'}
            socketIO.emit('fps_com', msg)
    else:
        # print 'Failed: enroll storage is full'
        msg = {'msg':'Failed: enroll storage is full'}
        socketIO.emit('fps_com', msg)


if __name__ == '__main__':
    fps =  FPS.FPS_GT511C3(device_name=DEVICE_GPIO,baud=9600,timeout=2,is_com=False)
    fps.UseSerialDebug = False
    GPIO.setmode(GPIO.BCM)      # programming the GPIO by BOARD pin numbers, GPIO21 is called as PIN21
    # Set the LED GPIO number
    LED = 21

    # Set the LED GPIO pin as an output
    GPIO.setup(LED, GPIO.OUT)             # initialize digital pin21 as an output.
    # fps.UseSerialDebug = True


    #fps.SetLED(True) # Turns ON the CMOS LED
    FPS.delay(1) # wait 1 second for initialize finish
    fps.SetLED(True) # Turns ON the CMOS LED

    while True:
        while fps.IsPressFinger() == False:
            FPS.delay(FPS.INTERVAL+0.03)
            socketIO.on('fps_com', on_fps_com_response)
            socketIO.wait(0.05)
            # print("i'm here",socket_cmd)
            if socket_cmd == 'add':
                # print('add')
                LegacyEnroll(fps)
                FPS.delay(2) # wait 1 second
                socket_cmd = 'none'
            elif socket_cmd == 'delete':
                print('delete')
                fps.DeleteID(int(socket_data))
                socketIO.emit('fps_com', {'msg':'Delete Successfull','data':socket_data})
                socket_cmd = 'none'

        idenid = identifyprotocol(fps)
        print 'lift the finger'
        socketIO.on('fps_com', on_fps_com_response)
        if  0 <= idenid < 200:
            socketIO.emit('fps_com', {'msg':'verified Successfull','data':idenid})
            GPIO.output(LED,True)                      # turn the LED on (making the voltage level HIGH)
            time.sleep(3.5)                         # sleep for a second
            GPIO.output(LED,False)                        # turn the LED off (making all the output pins LOW)
        else:
            socketIO.emit('fps_com', {'msg':'verified Failed','data':idenid})
        waitUntilRelease(fps)

    fps.SetLED(False) # Turns CLOSE the CMOS LED

    # fps.Close() # Closes serial connection
    pass
