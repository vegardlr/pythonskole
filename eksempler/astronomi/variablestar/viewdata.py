import sys
import numpy as np
from astropy.time import Time
import matplotlib.pyplot as plt


if len(sys.argv) < 2:
    print("Usage: getdata.py datafolder")
    sys.exit(1)

datafolder = sys.argv[1]
datafile = datafolder+"/data.txt"

f = open(datafile,'r')
data = np.genfromtxt(f,delimiter='\t')

tid = Time(data[:,0],format='jd').to_value('datetime64')
mag = data[:,1]

plt.plot(tid,mag,'.')
plt.xlabel("Tid")
plt.ylabel("Mag")
plt.title(datafolder)
ax = plt.gca()
ax.invert_yaxis()
plt.show()


#ps = np.abs(np.fft.fft(mag))**2
#time_step = 1 / 30
#freqs = np.fft.fftfreq(data.size, time_step)
#idx = np.argsort(freqs)
#plt.plot(ps)
#plt.show()
