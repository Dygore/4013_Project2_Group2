Ser = serial.Serial('COM3',9600)
While ser.in_waiting != 0:
ser.read()
