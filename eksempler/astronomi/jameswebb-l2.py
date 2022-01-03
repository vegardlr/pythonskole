import numpy as np

AU      = 149.6 * 10**9 #in m
G       = 6.67  * 10**(-11) #unit
M_sun   = 1.989 * 10**30 #in kg

M_earth = 5.972 * 10**24#in kg
V_earth = 29.78 * 10**3 #in m/s 
R_earth = 149.6 * 10**9 #in m

M_james = 1500.0        #in kg
R_james = 151.1 * 10**9 #in m
V_james = v_earth * ( R_james / R_earth )


M  = M_sun
me = M_earth
pe = np.array([R_earth,0.0])
ve = np.array([0.0,V_earth])
mj = M_james
pj = np.array([R_james,0.0])
vj = np.array([0.0,V_james])


while True:
    Rjs = np.abs(pj) 
    Res = np.abs(pe)
    Rje = np.abs(pj-pe)

    Fjs = G*M*mj/Rjs**2
    Fes = G*M*me/Res**2
    Fje = G*me*mj/Rje**2

    #Find components

