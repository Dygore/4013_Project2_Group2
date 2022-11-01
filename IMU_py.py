# Raspberry Pi Pico w BNO055
# import machine
import time
import board
import busio
import adafruit_bno055
# from bno055_base import BNO055_BASE

i2c = busio.I2C(board.GP15, board.GP14, frequency=400000)
sensor = adafruit_bno055.BNO055_I2C(i2c)

while True:
  print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
  print("Magnetometer (microteslas): {}".format(sensor.magnetic))
  print("Gyroscope (rad/sec): {}".format(sensor.gyro))
  print()

  time.sleep(1)






# i2c = machine.I2C(-1, scl=machine.Pin(2), sda=machine.Pin(0))
# imu = BNO055_BASE(i2c)
# calibrated = False
# while True:
#     time.sleep(1)
#     if not calibrated:
#         calibrated = imu.calibrated()
#         print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
#     print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
#     print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
#     print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))

