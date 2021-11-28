# SIMULERING MED TYNGDEKRAFT I PYTHON
# Pythonskole.no 30.11.2021
#
# Versjon 2: Ellipsebaner av ett legeme i bane rundt et stort

#Installer pythonskole på ditt system med: 
#  pip install pythonskole
#Importer pythonskole.astronomi sin Tyngdekraft-funksjon
from pythonskole.astronomi import Tyngdekraft

# Lag ditt 2D-rom, og bestem: 
#  - størrelsen L (hvor stor boksen skal være, LxL)
#  - Hvilken tittel du vil ha skrevet i plottevinduet
modell = Tyngdekraft(L=20.0,tittel="Planet og komet")

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

modell.nyttObjekt(midten,[0,0],200.)
modell.nyttObjekt(midten+[-5.0,0],[0,2.0],30.)
modell.nyttObjekt(midten+[+8.0,0],[0,-0.7],3.)

#Start simulering
modell.start()


