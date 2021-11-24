
# SIMULERING MED TYNGDEKRAFT I PYTHON
# KJØRT PÅ EN HELT VANLIG LAPTOP :)
# Pythonskole.no 25.11.2021
#
# Versjon 1: Lag en sky med mange små asteroider, og to planeter. 

# Importer noen utvalgte funksjoner fra numpy
# som vi trenger for å lage lister med tall (arrays), 
# tilfeldige tall (random) og til å beregne vinkler
# og komponenter
from numpy import array, random, sin, cos, pi

#Importer pythonskole for å bruke Tyngdekraft-modulen
from pythonskole import Tyngdekraft

# Lag ditt 2D-rom, og bestem størrelsen L 
# (boksen blir da LxL stor)
modell = Tyngdekraft(L=20.0,tittel="Sky")

# Kopier posisjonen i midten av boksen, som heter midten, 
# og boksens størrelse L
L = modell.L
midten = modell.midten

# Legg til et stort objekt med stor radius (størrelse)
# og sett den i midten
modell.nyttObjekt(midten,[0,0],200.)
# Legg til to middels objekt like til 
# venstre og høyre for midten...
modell.nyttObjekt(midten+[-2.0,0],[0,3.0],30.)
modell.nyttObjekt(midten+[+2.0,0],[0,-3.0],30.)

#Legg til mange små satser, ved å gjenta de neste linjene med
#kode mange ganger. Hver gang trekkes verdier for posisjon, 
#hastighet og størrelse fra en tilfeldig tallgenerator. 
for i in range(10):

    #Hvert objekt får radius som er trukket fra et tilfeldig tall
    #mellom 1.0 og 1.5
    radius    = random.uniform(1.0,1.5) 

    #Hvert objekt blir plassert i en avstand fra midten som 
    #er et tilfeldig tall mellom 0.1*L og 0.5*L
    avstand   = random.uniform(0.1*L,0.5*L)

    #Hvert objekt får en tilfeldig fart (i absolutt størrelse, 
    #foreløpig uten retning) som er gitt av objektets størrelse og 
    #avstand til midten
    fart      = 7.0*radius/avstand

    #Retningen farten får er bestemt av en vinkel, som også trekkes 
    #som et tilfeldig tall mellom 0 og 360 grader. Vinkelen er gitt
    #i radianer, så derfor er tallet mellom 0 og 2pi
    vinkel    = random.uniform(0.0,2.0*pi)

    #Vinkelen brukes også til å velge hvor rundt midten objektet 
    #plasseres, slik at hastigheten står 90 grader på en linje mellom 
    #objektet og midten. Her regner vi ut hvilke koordinater hvert 
    #objektet da får, gitt av avstand og vinkel
    posisjon  = midten + array([avstand*cos(vinkel), avstand*sin(vinkel)])

    #Hastigheten beregnes som en vektor, gitt av farten og vinkelen
    hastighet = array([fart*sin(vinkel), -fart*cos(vinkel)])

    #Objektet legges til i modellen, med de verdiene vi har regnet
    #ut for posisjon, hastighet og radius
    modell.nyttObjekt(posisjon, hastighet, radius)

#Start simulering
modell.start()


