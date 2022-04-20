
#Data: http://mizar.voksenlia.net/Variable/Redukvis/U-gem/

from pylab import *
#from datetime import datetime
import datetime
from astropy.time import Time

def jdtodt(jd):
    return datetime.datetime.strptime(str(jd),'%Y%j')


f = open("U-gem/data.txt","r")
data = genfromtxt(f,delimiter="\t")
t = Time(data[:,0],format='jd').to_value('datetime64')
mag = data[:,1]
print(t[0])

plot(t,mag)
show()

#print(t[0].to_value('datetime64'))
#print(jdtodt(data[1,0]))
#plot(jdtodt(data[:,0]),data[:,1],'o-')

#show()


