# from adafruit_platformdetect import Detector
# 
# detector = Detector()
# 
# print("Chip id: ", detector.chip.id)
# print("Board id: ", detector.board.id)

import machine

#create I2C obj
i2c = machine.I2C(1, scl = machine.Pin(15), sda = machine.Pin(14))

#Print out any addresses found
devices = i2c.scan()

if devices:
    for d in devices:
        print(hex(d))
        
# address is default to addr = 0x28