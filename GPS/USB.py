import serial, sys, time, csv

port = "COM3"

baudrate = 115200

fields = ['Latitude', 'Longitude', 'Satellites', 'Height', 'Time']

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
                        print(data.decode("utf-8"))




