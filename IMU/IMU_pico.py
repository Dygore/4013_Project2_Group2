# Raspberry Pi Pico w BNO055
# CircuitPython not compatiable w MicroPython

from machine import Pin, I2C
import time
from bno055 import *

# address of IMU
addr = 0x28

# chip ID = 0xA0 = 1010_0000
# ACC_ID = 0xFB
# MAG_ID = 0x32
# GYR_ID = 0x0F

i2c = machine.I2C(1, scl = machine.Pin(15), sda = machine.Pin(14))
imu = BNO055(i2c)

# Strings to hold IMU values
accel = ""
gyro= ""
mag = ""
imu_output = []

def getIMUData(imu):
    
    imu_output_list = []

    mag_tuple = ",".join(str(item) for item in imu.mag())
#     print(type(mag_tuple))
#     print(mag_tuple)
#     mag_list = mag_tuple.split(',')
#     print(type(mag_list))
#     imu_output_list.append(mag_list)
    print("mag data:", mag_tuple)
    
    gyro_tuple = ",".join(str(item) for item in imu.gyro())
#     gyro_list = gyro_tuple.split(',')
#     imu_output_list.append(gyro_list)
    print("gyro data: ", gyro_tuple)

    accel_tuple = ",".join(str(item) for item in imu.accel())
#     accel_list = accel_tuple.split(',')
#     imu_output_list.append(accel_list)
    print("accel data: ", accel_tuple)
    
    
#     imu_output = ','.join(str(item) for item in imu_output_list)
    imu_output = mag_tuple + ',' + gyro_tuple + ',' + accel_tuple
    print("Full IMU output: ", imu_output)
#     print()
    
    return imu_output
    #end getIMUData
    
while True:
    getIMUData(imu)
    time.sleep(1)
    
#     print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
#     print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
#     print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
#     print()
    # end while loop



# I2C Frequency: 400,000Hz 
# I2C0 SCL Pin 9
# I2C0 SDA Pin 8
# I2C1 SCL Pin 7
# I2C1 SDA Pin 6

# mag() returns float vector (x,y,z) in uT
# accel() returns float vector (x,y,y) in m/s^2
# gyro() returns float vector (x, y, z) in deg/s

# accelerometer (accel): measure linear acceleration
# gyroscope (gyro): measure rotational rate
# magnetometer (mag): establishes cardinal direction