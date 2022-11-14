
import os
import board
import busio as io
import digitalio
import storage
import adafruit_sdcard
import csv
from time import sleep

SD_CS = board.GP13 
 

# Connect to the card and mount the filesystem.
spi = io.SPI(board.GP10, board.GP11, board.GP12) #(this line defines the SPI Bus, which is how data is transferred back and forth from the on the card) (this line could change based on the circuit connections)

cs = digitalio.DigitalInOut(SD_CS)

sdcard = adafruit_sdcard.SDCard(spi, cs) # this line creates an SD card object

vfs = storage.VfsFat(sdcard) # this line creates file system object

storage.mount(vfs, "/sd") # this line mounts the file system from the SD card



with open('filename.cvs' , 'w' , newline=' ') as filename2:
    
    
      fieldnames = ['Date', 'Time', 'Satellite', 'Latitude', 'Longitude', 'Elivation MSL (m)', , 'X Accel (m/s^2)', 'Y Accel (m/s^2)', 'Z Accel (m/s^2)', , 'X Mag(uT)', 'Y Mag(uT)','Z Mag(uT)', 'X Gyro(rps)', 'Y Gyro(rps)', 'Z Gyro(rps)']
      thewriter = csv.DictWriter(filename2, fieldnames = fieldnames) 
      thewriter.writeheader()
      while True:
            thewriter.writerow( {'Date' : 'GET DATA FROM OTHERS ABOUT DATE' , 'Time' : ' GET DATA FROM OTHERS ' , 'Satellites' : ' GET DATA FROM OTHERS' , 'Latitude' : ' GET DATA FROM OTHERS' , 'Longitude' : ' GET DATA FROM OTHERS' , 'Elivation MSL (m)' : ' GET DATA FROM OTHERS' , 'X Accel (m/s^2)' : ' GET DATA FROM OTHERS' , 'Y Accel (m/s^2)' : ' GET DATA FROM OTHERS' , 'Z Accel (m/s^2)' : ' GET DATA FROM OTHERS' , 'X Mag(uT)' : ' GET DATA FROM OTHERS' , 'Y Mag(uT)' : ' GET DATA FROM OTHERS' , 'Z Mag(uT)' : ' GET DATA FROM OTHERS ' , 'X Gyro(rps)' : ' GET DATA FROM OTHERS ' , 'Y Gyro(rps)' : ' GET DATA FROM OTHERS ' , 'Z Gyro(rps)' : ' GET DATA FROM OTHERS'})
            
            with open('filename.cvs' , 'r' ) as read_file:
            print(read_file.read())
