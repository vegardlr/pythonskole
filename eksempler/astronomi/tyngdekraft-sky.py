# SIMULERING MED TYNGDEKRAFT I PYTHON
# Pythonskole.no 26.11.2021
#
# Versjon 1: Lag en sky med mange små asteroider, og to planeter. 

#Installer pythonskole på ditt system med: 
#  pip install pythonskole
#Importer pythonskole.astronomi sin Tyngdekraft-funksjon
from pythonskole.astronomi import Tyngdekraft

# Importer noen utvalgte funksjoner fra numpy
# som vi trenger for å lage lister med tall (arrays), 
# tilfeldige tall (random) og til å beregne vinkler
# og komponenter
from numpy import array, random, sin, cos, pi


# Lag ditt 2D-rom, og bestem: 
#  - størrelsen L (hvor stor boksen skal være, LxL)
#  - Hvilken tittel du vil ha skrevet i plottevinduet
modell = Tyngdekraft(L=20.0,tittel="Tre store og en sky")

# Kopier verdiene for boksens størrelse L og koordinatene til
# midten av plottevinduet, for de tallene trenger vi flere ganger
# nå vi skal bestemme hvor planetene i simuleringen skal ligge. 
L = modell.L
midten = modell.midten

# Nå skal vi legge til objekter/planeter i modellen. Da 
# trenger vi funksjonen nyttObjekt som bruker følgende argumenter: 
#   modell.nyttObjekt(posisjon, fart, radius)
#     - posisjon er en vektor med to elementer (f.eks. [1,3])
#     - fart er en vektor med to elementer
#     - radius er et vanlig desimaltall

# Legg til et stort objekt i modellen. 
# Sett den i midten, gi den null fart og stor radius (200)
modell.nyttObjekt(midten,[0,0],200.)
# Legg til to middels store objekter like til 
# venstre og høyre for midten, og gi dem fart i y-retning
modell.nyttObjekt(midten+[-2.0,0],[0,3.0],30.)
modell.nyttObjekt(midten+[+2.0,0],[0,-3.0],30.)

#Legg til mange små objekter.
#Ved å gjenta de neste linjene med kode mange ganger. Til hver gang 
#et nytt objekt lages trekkes verdier for posisjon, hastighet og 
#størrelse som tilfeldige tall

for i in range(300): #Øk dette talletom du vil ha flere små-objekter

    #Hvert objekt får radius som er trukket fra et tilfeldig tall
    #mellom 1.0 og 1.5
    radius    = random.uniform(1.0,1.5) 

    #Hvert objekt blir plassert i en avstand fra midten som 
    #er et tilfeldig tall mellom 0.1*L og 0.5*L
    avstand   = random.uniform(0.1*L,0.5*L)

    #Hvert objekt får en tilfeldig fart (i absolutt størrelse, 
    #foreløpig uten retning) som er gitt av objektets størrelse og 
    #avstand til midten
    fart      = 6.0*radius*radius/avstand

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


