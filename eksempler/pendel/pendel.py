
#PENDEL - PYTHONSKOLE.NO
# SIMULERING OG PASCO-DATA

import time
import numpy as np
from pylab import *
#from luftmotstand import * #Luftmostand m/snordrag
from pasco import PASCOBLEDevice
import matplotlib.pyplot as plt



#ERFARINGER: Det ideelle oppsettet
# - Snorlengde opp til 2m OK
# - Utslag bær være større enn 20 grader
# - Lang pendel betinger lett snor (fiskensnøre) eller tungt lodd 
#   og dertil solid oppheng
# - Lodd bør skrus fast i bunn av aks.sensor

snor_lengde = 2.43
vinkel_grader = 25
maks_perioder = 5
device_id='469-773'
ymin = 8.0
ymax = 12.0
xmax = 16.0

#Konstanter til bruk i utregningene
pi = 3.14159
g  = 9.81             # Tyngdens akselerasjon
rho= 1.293          # Lufts tetthet
CD = 0.40            # En sfære har CD=0.45 
m  = 0.050            # Kulas masse
r  = 0.05             # Kulas radius
l  = snor_lengde     # Snorlengden
K  = rho*pi*r*r*CD/2 # Brukes i likning F=K*v*v

# Omega = vinkelhastighet
omega = []
# Theta = vinkelposisjon
theta = []
# Akselerasjon
aks_data= []
aks_sim=[]
# Tidssteg
steps = []
tid   = []
tid_forrige = 0.0


#Setter initial verdier til løkka
periode     = 0 # Teller for antall svingninger
omega_start = 0
theta_start = -pi*vinkel_grader/180


#Artist animation
#fig = figure()
#plots = []
#p, = plot(tid,aks_data)
#plots.append([p])


#ION
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(tid,aks_sim,lw=3,label="Simulering")
line2, = ax.plot(tid,aks_data,'-x',lw=3,label="PASCO data")
ax.set_xlim(0.,xmax)
ax.set_ylim(ymin,ymax)
ax.set_xlabel("Tid (s)")
ax.set_ylabel("Aks. ($m/s^2$)")
ax.legend()
fig.canvas.draw()
plt.pause(0.001)


device = PASCOBLEDevice()
device.connect_by_id(device_id)
print("Starter om 10 sekunder...")
time.sleep(7)
print("Klar")
time.sleep(1)
print("Ferdig")
time.sleep(1)
print("Gå")
time.sleep(0.2)

#Start simulering og måling
tid_start = time.time()
tid_forrige = tid_start
while periode<maks_perioder:
    
    #Kraftberegninger
    v=np.absolute(omega_start*l)       # Fart, absoluttverdi
    am = K*v*v*np.sign(omega_start)/m  # Luftmotstand
    #am = luftmotstand(omega_start)    # Luftmotstand m/snordrag
    alpha=(g*np.sin(theta_start)+am)/l # Vinkel akselerasjonen
    
    #Leser aksellerasjonsdata fra sensor
    verdi = device.read_data('Accelerationx')
    if not verdi == None:
        verdi = np.absolute(verdi)
    aks_data.append(verdi)
    tid_naa = time.time()
    dt = tid_naa-tid_forrige
    print("t=",round(tid_naa-tid_start,2),"s")
    
    #Integrere posisjon/hastighetsvariable
    omega_slutt = omega_start - alpha*dt
    theta_slutt = theta_start + omega_slutt*dt
    if omega_slutt>=0 and omega_start<0:
        periode = periode + 1  # Teller antall perioder pendelen har fullført.
        print("Fullført periode",periode)
    
    steps.append(dt)
    tid.append(tid_naa-tid_start)
    theta.append(theta_slutt)
    omega.append(omega_slutt)
    aks_sim.append(g*np.cos(theta_slutt) + l*omega_slutt**2)  #a=g*cos(t)+v²/r
    
    line1.set_xdata(tid)
    line1.set_ydata(aks_sim)
    line2.set_xdata(tid)
    line2.set_ydata(aks_data)
    fig.canvas.draw()
    plt.pause(0.01)

    theta_start=theta_slutt
    omega_start=omega_slutt
    tid_forrige = tid_naa

device.disconnect()

diffsum = 0.0
count = 0.0
for i in range(len(aks_data)):
    if (not aks_data[i] == None) and (not aks_sim[i] == None):
        count = count + 1
        diffsum = diffsum + np.absolute(aks_data[i]-aks_sim[i])

error_abs = round(diffsum/len(aks_data),2)
error_rel = round(diffsum/count/g,2)
print("Gjennomsnittlig absolutt feil:", error_abs)
print("Gjennomsnittlig relativ feil :", 100.0*error_rel,"%")

a = input("Animasjon ferdig. Lukk plot-vinduet og trykk enter for å fortsette...")


plt.ioff()
plt.plot(tid,aks_sim,label="Simulering")
plt.plot(tid,aks_data,'-x',label="PASCO-data")
plt.title("Klassisk pendel - Akselerasjon")
plt.legend()
plt.xlabel("Tid (s)")
plt.ylabel("Aks. ($m/s^2$)")
plt.show()


after_plot = False
if after_plot:
    plot(tid,aks_sim,label="Simulering")
    plot(tid,aks_data,'-x',label="PASCO-data")
    title("Klassisk pendel - Akselerasjon")
    legend()
    xlabel("Tid (s)")
    ylabel("Aks. ($m/s^2$)")
    show()

    dtmin  = min(steps)-0.05
    dtmaks = max(steps)+0.05

    plot(tid,steps,label="dt(t)")
    title("Klassisk pendel - Tidssteg")
    ylim(dtmin,dtmaks)
    xlabel("Tid (s)")
    ylabel("dt ($s$)")
    show()
