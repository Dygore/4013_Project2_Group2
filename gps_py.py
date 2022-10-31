#Import pins & UART from Pico
from machine import Pin, UART

#Import the time
import utime, time

#Set up Pico UART with baud of 9600 and TX/RX pins
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

#Array for output of GPS
buff = bytearray(255)

#If the data is timed out or invalid
timeout = False
Status = False

#Strings to hold output of UART Communication
latitude = ""
longitude = ""
satellites = ""
HeightGeo = ""
GPStime = ""

def getGPSData(gpsModule):
    global Status, timeout, latitude, longitude, satellites, GPStime, HeightGeo
    
    #Current time + 10 seconds
    timeout = time.time() + 10
    
    while True:
        #Read UART line
        gpsModule.readline()
        
        #Get second line and add it to buffer
        buffer = str(gpsModule.readline())
        
        #Split up buffer using commas
        section = buffer.split(',')
    
        #We only want GPGGA as it contains all the data that is needed for this project
        if (section[0] == "b'$GPGGA" and len(section) == 15):
            if(section[1] and section[2] and section[3] and section[4] and section[5] and section[6] and section[7] and section[8] and section[9]):
                print(buff)
                
                latitude = convertToDegree(section[2])
                if (section[3] == 'S'):
                    latitude = '-' + latitude
                longitude = convertToDegree(section[4])
                if (section[5] == 'W'):
                    longitude = '-' + longitude
                satellites = section[7]
                HeightGeo = section[7]
                GPStime = section[1][0:2] + ":" + section[1][2:4] + ":" + section[1][4:6]
                Status = True
                break
                
        if (time.time() > timeout):
            timeout = True
            break
        utime.sleep_ms(500)
        
def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)
    
    
while True:
    
    getGPSData(gpsModule)

    if(Status == True):
        print("Printing GPS data...")
        print(" ")
        print("Latitude: "+latitude)
        print("Longitude: "+longitude)
        print("Satellites: " +satellites)
        print("Height ASL Geoid: " + HeightGeo)
        print("Time: "+GPStime)
        print("----------------------")
        
        Status = False
        
    if(timeout == True):
        print("No GPS data is found.")
        timeout = False