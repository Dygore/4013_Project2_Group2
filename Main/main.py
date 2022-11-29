#-------------------------------Import from Pico-------------------------------
from machine import Pin, UART, I2C, SPI, PWM

#-------------------------------Other Imports-------------------------------
import utime, time
from bno055 import *

import sdcard, uos

#-------------------------------Initialize Serial Communcation-------------------------------
#----------GPS----------
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
#----------Bluetooth UART----------
#----------IMU I2C----------
i2c = I2C(0, scl=Pin(21), sda=Pin(20))
#----------SD Card SPI----------
cs = Pin(13, Pin.OUT)
spi = SPI(1,baudrate=100000,polarity=0,phase=0,bits=8,firstbit=SPI.MSB,sck=Pin(10),mosi=Pin(11),miso=Pin(12))
#-------------------------------Variable Declarations/Initializations-------------------------------
buzzer = PWM(Pin(8))
tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

song = ["E5","D5","C5","D5","E5","E5","E5","P","D5","D5","D5","E5","G5","G5","P","E5","D5","C5","D5","E5","E5","E5","P","E5","D5","D5","E5","D5","C5"]
#----------GPS----------
buff = bytearray(255)
timeout = False
Status = False
latitude = ""
longitude = ""
satellites = ""
HeightGeo = ""
GPStime = ""
ledg = Pin(14, Pin.OUT)
ledr = Pin(15, Pin.OUT)
magnet = Pin(27, Pin.IN)
#----------Bluetooth----------
#----------IMU----------
addr = 0x28
imu = BNO055(i2c)
accel = ""
gyro= ""
mag = ""
data = []

#----------SD Card----------
while True:
    try:
        sd = sdcard.SDCard(spi, cs)

        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd")
        break
    except:
        ledg.value(0)
        ledr.value(1)
    
fields = ['Latitude', 'Longitude', 'Satellites', 'Height', 'Time', 'Mag_X', 'Mag_Y', 'Mag_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Accel_X', 'Accel_Y', 'Accel_Z']
#-------------------------------Define Methods-------------------------------
#----------GPS----------
def getGPSData(gpsModule):
    global Status, latitude, longitude, satellites, GPStime, HeightGeo
    
    while True:
        #Get second line and add it to buffer
        buffer = str(gpsModule.readline())
        
        #Split up buffer using commas
        section = buffer.split(',')
    
        #We only want GPGGA as it contains all the data that is needed for this project
        if (section[0] == "b'$GPGGA" and section[4] != ''):
            latitude = convertToDegree(section[2])
            if (section[3] == 'S'):
                latitude = '-' + latitude
            longitude = convertToDegree(section[4])
            if (section[5] == 'W'):
                longitude = '-' + longitude
            satellites = section[7]
            HeightGeo = section[9]
            GPStime = section[1][0:2] + ":" + section[1][2:4] + ":" + section[1][4:6]
            Status = True
            #Set LED to Signal Found
            ledg.value(1)
            ledr.value(0)
            break
        elif (section[0] == "b'$GPGGA" and section[4] == '') :
            #Set LED to Searching for Signal
            ledg.value(0)
            ledr.value(1)    
        utime.sleep_ms(100)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

#----------Bluetooth----------

#----------IMU----------
def getIMUData(imu):
    global mag_tuple, gyro_tuple, accel_tuple

    mag_tuple = ",".join(str(item) for item in imu.mag())
    
    gyro_tuple = ",".join(str(item) for item in imu.gyro())

    accel_tuple = ",".join(str(item) for item in imu.accel())
    
#----------SD Card----------
def sdCard():
    global latitude, longitude, satellites, GPStime, HeightGeo, mag_tuple, gyro_tuple, accel_tuple
    while True:
        try:
            logf = open("/sd/logfile.csv","a")
            logf.write(latitude)
            logf.write(",")
            logf.write(longitude)
            logf.write(",")
            logf.write(satellites)
            logf.write(",")
            logf.write(HeightGeo)
            logf.write(",")
            logf.write(GPStime)
            logf.write(",")
            logf.write(mag_tuple)
            logf.write(",")
            logf.write(gyro_tuple)
            logf.write(",")
            logf.write(accel_tuple)
            logf.write("\r\n")
            logf.close()
            break
        except:
            ledg.value(0)
            ledr.value(1)

#----------Buzz----------
def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for i in range(len(mysong)):
        if (mysong[i] == "P"):
            bequiet()
        else:
            playtone(tones[mysong[i]])
        utime.sleep_ms(300)
    bequiet()
    
#-------------------------------Main Methods-------------------------------
logf = open("/sd/logfile.csv","a")
try:
    logf.write("Latitude")
    logf.write(",")
    logf.write("Longitude")
    logf.write(",")
    logf.write("Satellites")
    logf.write(",")
    logf.write("HeightGeo")
    logf.write(",")
    logf.write("GPS Time")
    logf.write(",")
    logf.write("Mag_X")
    logf.write(",")
    logf.write("Mag_Y")
    logf.write(",")
    logf.write("Mag_Z")
    logf.write(",")
    logf.write("Gryo_X")
    logf.write(",")
    logf.write("Gyro_Y")
    logf.write(",")
    logf.write("Gyro_Z")
    logf.write(",")
    logf.write("Accel_X")
    logf.write(",")
    logf.write("Accel_Y")
    logf.write(",")
    logf.write("Accel_Z")
    logf.write("\r\n")
except OSError:
    print("Sd Full")
logf.close()

while True:
    #Get GPS Data
    getGPSData(gpsModule)
    #Get IMU Data
    getIMUData(imu)
        
    #Output to USB
    if(Status == True):
         print("{"+ latitude + ',' + longitude + ',' + satellites + ',' + HeightGeo + ',' + GPStime + ',' + mag_tuple + ',' + gyro_tuple + ',' + accel_tuple +"\n")   
         Status = False
         
    #SD Card
    sdCard()
    #Output to Bluetooth
    
    if magnet.value() == 0:
        ledg.value(0)
        ledr.value(1)
        playsong(song)
    
