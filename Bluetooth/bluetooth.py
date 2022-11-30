from machine import Pin, UART
import utime, time
# uart = UART(0,baudrate = 38400, tx = Pin(1), rx = Pin(2)) #UART(port #, baud rate)
uart = UART(0, baudrate = 9600)

while True:
    data = "testing"
#     print(data)
    uart.write(data + '\r\n')
    utime.sleep_ms(100)
#     uart.writeline(data + '\r\n')
    #/r to reset cursor to the left
    #/n to create new line
    #'/r/n' are for visual understanding