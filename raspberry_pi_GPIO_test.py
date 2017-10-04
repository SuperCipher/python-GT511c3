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


'''
import FPS, sys
DEVICE_GPIO = '/dev/ttyAMA0'
# DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
# DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
# DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 9600
FPS.DEVICE_NAME = DEVICE_GPIO

def waitUntilPress(fps):
    while fps.IsPressFinger() == False:
        FPS.delay(FPS.INTERVAL+0.003)

def waitUntilRelease(fps):
    while fps.IsPressFinger() == True:
        FPS.delay(FPS.INTERVAL+0.003)

def identifyprotocol(fps):
    waitUntilPress(fps)
    if fps.CaptureFinger(True):
        return fps.Identify1_N()
    else:
        return fail

def LegacyEnroll(fps):
    '''
    Enroll test
    '''

    enrollid=0
    okid=True
    #search for a free enrollid, you have max 200
    while okid == True and enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print okid
        if okid == True:
            enrollid+=1
    if enrollid <200:
        #press finger to Enroll enrollid
        print 'Press finger to Enroll %s' % str(enrollid)
        fps.EnrollStart(enrollid)
        waitUntilPress(fps)
        iret = 0
        if fps.CaptureFinger(True):
            #remove finger
            print 'remove finger'
            fps.Enroll1()
            waitUntilRelease(fps)
            #Press same finger again
            print 'Press same finger again'
            waitUntilPress(fps)
            if fps.CaptureFinger(True):
                #remove finger
                print 'remove finger'
                fps.Enroll2()
                waitUntilRelease(fps)
                #Press same finger again
                print 'press same finger yet again'
                waitUntilPress(fps)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    if iret == 0:
                        print 'Enrolling Successfull'
                    else:
                        print 'Enrolling Failed with error code: %s' % str(iret)
                else:
                    print 'Failed to capture third finger'
            else:
                print 'Failed to capture second finger'
        else:
            print 'Failed to capture first finger'
    else:
        print 'Failed: enroll storage is full'


if __name__ == '__main__':
    fps =  FPS.FPS_GT511C3(device_name=DEVICE_GPIO,baud=9600,timeout=2,is_com=False)
    fps.UseSerialDebug = False
    # fps.UseSerialDebug = True
    fps.SetLED(True) # Turns ON the CMOS LED
    FPS.delay(1) # wait 1 second for initialize finish

    # waitUntilPress(fps)
    # waitUntilRelease(fps)

    # LegacyEnroll(fps)
    # print 'Identify'
    # FPS.delay(1)
    print identifyprotocol(fps)

    # fps.DeleteAll()

    fps.SetLED(False) # Turns CLOSE the CMOS LED

    # fps.Close() # Closes serial connection
    pass
