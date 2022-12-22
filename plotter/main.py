import serial
from tqdm import tqdm
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

sample_name = ''
if len(sys.argv) > 1:
    sample_name = sys.argv[1]

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

# Set the serial port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 2000000

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

        # Collect 4096 samples
        for i in tqdm(range(4096), desc='Logging Data'):
            # Read a line of data from the serial port
            line = ser.readline()

            # Split the line into a list of values
            values = line.split(b',')

            # Convert the values to integers
            try:
                values = [float(x) for x in values]
            except ValueError:
                # If a value cannot be converted to an integer, skip this iteration
                continue

            # Check that we have received the correct number of values
            if len(values) != 4:
                # If the number of values is incorrect, skip this iteration
                continue

            # Write the values to the CSV file
            writer.writerow(values)

except IOError:
    print('Error: Could not open CSV file for writing')
    exit()

# Close the serial port when we are done
ser.close()

with open(csv_file_name, 'r') as f:
  reader = csv.reader(f)
  next(reader)  # skip the header row
  data = []
  for row in reader:
    data.append(row)

# convert the data to a NumPy array
data = np.array(data, dtype=float)

time = data[:, 0]*1e-6
ax = data[:, 1]
ay = data[:, 2]
az = data[:, 3]

sp_int = np.diff(time)
sp_mean = np.mean(1/sp_int)
sp_var = np.var(1/sp_int)
print("Sampling frequency mean: {}".format(sp_mean))
print("Sampling frequency variance: {}".format(sp_var))

# time = np.linspace(0,10,1000)
# ay = np.sin(2*np.pi*5*time)
# ax = np.sin(2*np.pi*5*time)
# az = np.sin(2*np.pi*5*time)
# sp_mean=1/(10/1000)

plt.plot(time,ax,label='time_ax')
plt.plot(time,ay,label='time_ay')
plt.plot(time,az,label='time_az')
plt.legend()
plt.title("Time vs Acceleration")
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [m/s^2]")
plt.show()
plt.savefig('time_response.png')

N = len(time)
ax_fft = np.fft.fft(ax)
ay_fft = np.fft.fft(ay)
az_fft = np.fft.fft(az)

plt.plot(np.linspace(0,sp_mean/2,N/2-1),abs(ax_fft[1:int(N/2)]/N)*2, label='fft_ax')
plt.plot(np.linspace(0,sp_mean/2,N/2-1),abs(ay_fft[1:int(N/2)]/N)*2, label='fft_ay')
plt.plot(np.linspace(0,sp_mean/2,N/2-1),abs(az_fft[1:int(N/2)]/N)*2, label='fft_az')
plt.legend()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Amplitude")
plt.show()
plt.savefig('frequency_response.png')
