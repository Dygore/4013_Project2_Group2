#-------------------------------Import from Pico-------------------------------
from machine import Pin, UART, I2C, csv

#-------------------------------Other Imports-------------------------------
import utime, time
from bno055 import *
import sdcard
import uos

#-------------------------------Initialize Serial Communcation-------------------------------
#----------GPS----------
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
#----------Bluetooth UART----------
#----------IMU I2C----------
i2c = I2C(1, scl=Pin(21), sda=Pin(26))
#----------SD Card SPI----------
cs = Pin(13, Pin.OUT)
spi = SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=SPI.MSB,sck=Pin(10),mosi=Pin(11),miso=Pin(12))
#-------------------------------Variable Declarations/Initializations-------------------------------
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
#----------Bluetooth----------
#----------IMU----------
addr = 0x28
imu = BNO055(i2c)
accel = ""
gyro= ""
mag = ""
data = []
#----------SD Card----------
sd = sdcard.SDCard(spi, cs)

vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

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
        if (section[0] == "b'$GPGGA" and section[7] != '00'):
            print(section)
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
        else :
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

    mag_tuple = ",".join(str(item) for item in imu.mag())
    
    gyro_tuple = ",".join(str(item) for item in imu.gyro())

    accel_tuple = ",".join(str(item) for item in imu.accel())
    
#----------SD Card----------

#-------------------------------Main Methods-------------------------------
def main:
    
    with open("/sd/Project_2_data.csv", 'a',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvfile.flush()
        
    while True:
    
    #Get GPS Data
    getGPSData(gpsModule)
    #Get IMU Data
    getIMUData(imu)
    
    data = [latitude,longitude, satellites, HeightGeo, GPStime, mag_tuple, gyro_tuple, accel_tuple]
    
    #Output to USB
    if(Status == True):
        print("{"+ data +"\n")   
        Status = False
        
    #Output to Bluetooth
        
    #Output to SD Card
    with open("/sd/Project_2_data.csv", 'a', newline='') as csvfile:
        csvwriter.writerow(data.split(","))
        csvfile.flush()
    
