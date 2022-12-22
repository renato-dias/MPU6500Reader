import csv
import numpy as np
import matplotlib.pyplot as plt

with open('./../samples/simpleTest.txt', 'r') as f:
  reader = csv.reader(f)
  next(reader)  # skip the header row
  data = []
  for row in reader:
    data.append(row)

# convert the data to a NumPy array
data = np.array(data, dtype=float)

time = data[:, 0] * 1e-6
ax = data[:, 1]
ay = data[:, 2]
az = data[:, 3]

sp_int = np.diff(time)
sp_mean = np.mean(1/sp_int)
sp_var = np.var(1/sp_int)
print("Sampling frequency mean: {}".format(sp_mean))
print("Sampling frequency variance: {}".format(sp_var))

N = len(time)
ax_fft = np.fft.fft(ax)
ay_fft = np.fft.fft(ay)
az_fft = np.fft.fft(az)

plt.plot(time,ax,label='time_ax')
plt.plot(time,ay,label='time_ay')
plt.plot(time,az,label='time_az')
plt.legend()
plt.title("Time vs Acceleration")
plt.xlabel("Time [us]")
plt.ylabel("Acceleration [m/s^2]")
plt.show()
plt.savefig('time_response.png')

plt.plot(np.linspace(0,sp_mean,N),ax_fft, label='fft_ax')
# plt.plot(ay_fft, label='ay')
# plt.plot(az_fft, label='az')
plt.legend()
plt.show()
plt.savefig('frequency_response.png')
