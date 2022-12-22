import csv
import serial
import sys
from datetime import datetime

sample_name = ''
if len(sys.argv) > 1:
    sample_name = sys.argv[1]

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

# Set the serial port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Open the serial port
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
except serial.serialutil.SerialException:
    print('Error: Could not open serial port')
    exit()

csv_file_name = '{}_{}.csv'.format(dt_string, sample_name)
print(csv_file_name)

# Open the CSV file for writing
try:
    with open(csv_file_name, 'w+', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['time_ms', 'accel_x_mps2', 'accel_y_mps2', 'accel_z_mps2'])

        while True:
            # Read a line of data from the serial port
            line = ser.readline()

            # Split the line into a list of values
            values = line.split(b',')

            # Convert the values to integers
            try:
                values = [float(x) for x in values]
            except ValueError:
                # If a value cannot be converted to an integer, skip this line
                continue

            # Check that we have received the correct number of values
            if len(values) != 4:
                # If the number of values is incorrect, skip this line
                continue

            # Write the values to the CSV file
            writer.writerow(values)

except IOError:
    print('Error: Could not open CSV file for writing')
    exit()

# Close the serial port when we are done
ser.close()