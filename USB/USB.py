import serial, sys, time, csv

port = "COM3" #COM port Select

baudrate = 115200

fields = ['Latitude', 'Longitude', 'Satellites', 'Height', 'Time', 'Mag_X', 'Mag_Y', 'Mag_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Accel_X', 'Accel_Y', 'Accel_Z']

filename = "Project_2_Data.csv"

ser = serial.Serial(port,baudrate)

with open(filename, 'a', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvfile.flush()
        
        while True:
                data = ""
                if (ser.read(1) == b'{'):
                        data = ser.read_until(b'\r')
                        csvwriter.writerow(data.decode("utf-8").split(","))
                        csvfile.flush()




