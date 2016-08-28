#!/usr/bin/env python
import smbus
import time
from pyfingerprint.pyfingerprint import PyFingerprint
import sys
import string
import binascii
import time
import datetime
import RPi.GPIO as GPIO
from sqldb import *
from subprocess import call
import requests


DB = SQLDatabase("fingerprint")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, 0)
time.sleep(1)
GPIO.output(4, 1)
time.sleep(2)
GPIO.output(4, 0)


# connecting to fingerprint
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

## Gets some sensor information
print('Currently stored templates: ' + str(f.getTemplateCount()))



# Define some device parameters
I2C_ADDR  = 0x3F # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1



def getTimeStampFileName ():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d%H_%M_%S.jpg')
    return st


def sendTextMessage ( data ):
    num = DB.getSMS()
    mobile_num = num[0]['mobile_number']
    
    cmd = ["/usr/bin/gammu-smsd-inject" , "-c" , 
          "/etc/gammu-smsdrc", "TEXT", "%s" % mobile_num,
          "-text" , "%s" % data ]
    print "command : ", cmd
    call(cmd)


def takesnapshot():
    requests.get("http://localhost:8082/0/action/snapshot")
    # copy file to images folder
    filename = getTimeStampFileName()
    filepath = "/home/pi/sandbox/fingerprintweb/public/images/%s" % filename
    call(["cp", "/tmp/motion/lastsnap.jpg", filepath])
    return filename


def snapshot(type , note):
    filename = takesnapshot()
    epoch_time = DB.insertImage(filename)
    image = "%s/%s"% (epoch_time, filename)
    DB.insertActivity(type, note, image)
    image_url = "http://192.168.10.88/image/%s" % image
    return image_url


def lcd_init():
    # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
    time.sleep(E_DELAY)

def lcd_string(message,line):
    # Send string to display

    message = message.ljust(LCD_WIDTH," ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
       lcd_byte(ord(message[i]),LCD_CHR)


def finger_enrolment( f, data ): 
    lcd_string("Enrolment for ",LCD_LINE_1)
    lcd_string(data['name'],LCD_LINE_2)
    time.sleep(3)
   
    lcd_string("Waiting for",LCD_LINE_1)
    lcd_string("   Finger",LCD_LINE_2)

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass


    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        lcd_string("Error: ",LCD_LINE_1)
        lcd_string("Finger Exists!",LCD_LINE_2)
        #return 0

    lcd_string("Please remove ",LCD_LINE_1)
    lcd_string("Finger",LCD_LINE_2)
    time.sleep(2)
    lcd_string("Waiting for ",LCD_LINE_1)
    lcd_string("the same Finger",LCD_LINE_2)
 
    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass


    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(0x02)

    ## Compares the charbuffers and creates a template
    f.createTemplate()

    ## Saves template at new position number
    if ( f.storeTemplate(data['id']) == True ):
        print('Finger enrolled successfully!')
        lcd_string("Finger enrolled",LCD_LINE_1)
        lcd_string("successfully",LCD_LINE_2)
        print('New template position #' + str(data['id']))

    time.sleep(2)

    lcd_string("Finger security ",LCD_LINE_1)
    lcd_string("     Mode",LCD_LINE_2)
    return 1


def finger_search(f):
    lcd_string("Finger security ",LCD_LINE_1)
    lcd_string("     Mode",LCD_LINE_2)

    for x in range (0, 50):
        ## Wait that finger is read
        if f.readImage() == True :
            f.convertImage(0x01)
            lcd_string("Got fingerprint ",LCD_LINE_1)
            lcd_string("   Checking...",LCD_LINE_2)
            time.sleep(1)
            ## Searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                lcd_string("No Match ",LCD_LINE_1)
                lcd_string("   Found...",LCD_LINE_2)
                time.sleep(1)
                lcd_string("Taking picture",LCD_LINE_1)
                lcd_string("of intruder...",LCD_LINE_2)
                image_url = snapshot("intruder", "Someone is trying to access ")
                data = "Someone is trying to access. %s" % image_url
                sendTextMessage ( data )
                return 0
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))
                # get the data for the finger
                match = DB.isIdExists(positionNumber, "FDATA")
                print match
                lcd_string("Good Day! ",LCD_LINE_1)
                lcd_string(match[1],LCD_LINE_2)
                time.sleep(1)
                image_url = snapshot("entry", "%s has entered the facility" % match[1])
                data = "%s has entered the facility. %s" % ( match[1], image_url)
                sendTextMessage ( data )
                lcd_string("Opening lock ",LCD_LINE_1)
                lcd_string("for 3 seconds" ,LCD_LINE_2)
                GPIO.output(4, 1)
                time.sleep(3)
                GPIO.output(4, 0)
                lcd_string("Thank you ",LCD_LINE_1)
                lcd_string("and Good Day!",LCD_LINE_2)


    


def main():
    # Main program block

    # Initialise display
    lcd_init()
    # Send some test
    print "writing to lcd"
    lcd_string("Fingerprint    <",LCD_LINE_1)
    lcd_string("   operational <",LCD_LINE_2)
    time.sleep(1)
    while True:
        # check if there is data for enrolment
        # if yes goto enrolment phase
        enrol = DB.getEnrol()
        if enrol[0]['id'] != 0:
            print "Enrolment phase"
            time.sleep(2)
            finger_enrolment( f, enrol[0] )
            DB.updateEnrol(0, "done")
            continue
        
        # if not wait for fingerprint image
        finger_search(f)    

        time.sleep(2)

  


main()
print "hello"
while True:
    # do nothing
    x = 1
