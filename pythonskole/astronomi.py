###   Pythonskole.no    Tyngdekraft    ###
###   28.11.2021  kontakt@pythonskole.no ###

import sys # TODO Remove this on publish
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation

######################
######################
### INITIALIZATION ###
######################
######################

class Tyngdekraft():
    def __init__(self,dt=0.03,L=20.0, tittel = 'Tyngdekraft'):
        self.tstep = 0
        self.dt = dt
        self.n = 0
        self.L = L
        self.interval=10
        self.center = np.array([0,0])
        self.midten = self.center
        self.cog = self.center
        self.title = tittel
        self.activate_collisions = False
        self.diagnostic_output = False
        self.follow_center_of_gravity = False
        self.exit_at_next_iteration = False

    def nyttObjekt(self,pos,vel,mass):
        datatype = np.dtype([
            ('pos', np.float64 , 2),('vel', np.float64 , 2),
            ('acc', np.float64 , 2),('force', np.float64 , 2),
            ('mass', np.float64 , 1),('size', np.float64 , 1)])
        new = np.zeros(1,dtype=datatype) 
        new["pos"]   = pos
        new["vel"]   = vel
        new["acc"]   = np.zeros(2)
        new["force"] = np.zeros(2)
        new["mass"]  = mass
        new["size"]  = self.sizeFromMass(mass)
        if self.n > 0:
            self.obj = np.append(self.obj,new)
        else:
            self.obj = new 
        self.n = len(self.obj)
 

######################
######################
###  INTEGRATIONS  ###
######################
######################

    def calculate_forces(self):
        # Use linear algebra to calculate the forces acting 
        # between each and every planet in the simulation, 
        # using the N-body method. 
        gravity_factor = 0.1
        ones = np.ones(self.n)
        # Get mass and positions of planets
        m = self.obj["mass"][:]
        x = self.obj["pos"][:,0]
        y = self.obj["pos"][:,1]
        # Calculate discances between each particle and product of masses
        dx = np.outer(ones,x) - np.outer(x,ones)
        dy = np.outer(ones,y) - np.outer(y,ones)
        m2 = np.outer(ones,m) * np.outer(m,ones)
        d = np.sqrt(dx**2 + dy**2)
        np.fill_diagonal(d,np.inf)
        # Calculate gravity, angle between positions, and force components
        f  = gravity_factor*m2/d  #3D: gravity_factor*m2/d2
        theta = np.arctan2(dy, dx)
        fx = np.sum(f * np.cos(theta),1)
        fy = np.sum(f * np.sin(theta),1)
        #Save force and acceleration acting on each planet
        self.obj["force"] = np.transpose(np.vstack((fx,fy)))
        self.obj["acc"]   = np.transpose(np.vstack((fx/m,fy/m)))

    def sizeFromMass(self,mass):
        #Scaling so that scatter-objects are in units 
        # of plot coordinates, not window size (pixels) 
        size_to_mass_ratio = 100.0/self.L**2
        return mass*size_to_mass_ratio
    
    def radiusFromSize(self,size):
        size_to_radius_ratio = 0.02  #OLD TESTED VALUE 0.016
        return size_to_radius_ratio*np.sqrt(size)

    #Collisions module need more work before it is safe to use
    #It is per now deactivated (in function update())
    def handle_collisions(self):
        size_factor = 0.004
        ones = np.ones(self.n)
        # Get positions of all the planets
        x = self.obj["pos"][:,0]
        y = self.obj["pos"][:,1]
        # Calculate discances between each planet
        deltax = np.outer(ones,x) - np.outer(x,ones)
        deltay = np.outer(ones,y) - np.outer(y,ones)
        delta2 = deltax**2 + deltay**2
        np.fill_diagonal(delta2,np.inf)
        # Is their size larger than their distance?
        r = self.radiusFromSize(self.obj["size"][:])
        rsum2 = (np.outer(ones,r) + np.outer(r,ones))**2
        # Count all planets that has collided
        collisions = np.tril(delta2 <= rsum2)
        #print("----------------")
        #vx = self.obj["vel"][:,0]
        #vy = self.obj["vel"][:,1]
        #print("d2:",delta2)
        #print("r2:",rsum2)
        #print("vx:",vx)
        #print("vy:",vy)
        if np.sum(collisions) == 0: 
            return 

        indices = np.column_stack(np.where(collisions))
        #print("COLLISION")
        #print(" i: ",indices)
        #for ind in indices: 
        #    print("ind:",ind)
        #    for i in ind:
        #        print("i:",i)
        #        print("delta2;",delta2[i])
        #        print("rsum2:",rsum2[i])
        #        print("vx:",vx[i])
        #        print("vy:",vy[i])
        #self.exit_at_next_iteration = True
        print("indices:",indices,self.n)
        delete= []
        for ind in indices:
            self.collide(ind)
            delete.append(ind[1])
        for i in delete: 
            self.obj = np.delete(self.obj,i)
        self.n = len(self.obj)
        print("delete:",delete,self.n)

    def collide(self,ind):
        msum = np.sum(self.obj["mass"][ind])
        psum = np.sum(self.obj["vel"][ind]*self.obj["mass"][ind],0)
        ##COLLISION DIAGNOSTICS KEPT FOR NOW
        #print("COLLIDE")
        #print(" ind:",ind)
        #print(" m:",self.obj["mass"][ind])
        #print(" msum:",msum)
        #print(" p:",self.obj["vel"][ind]*self.obj["mass"][ind])
        #print(" psum:",psum)
        self.obj["mass"][ind[0]] = msum
        self.obj["size"][ind[0]] = self.sizeFromMass(msum)
        self.obj["vel"][ind[0],:] =  psum / msum
        self.obj["force"][ind[0],:] = np.zeros(2)
        self.obj["acc"][ind[0],:] = np.zeros(2)

    def integrate_orbits(self):
        if self.n == 0:
            raise ValueError('No more objects')

        self.tstep += 1
        self.obj["vel"]=self.obj["vel"]+self.obj["acc"]*self.dt
        self.obj["pos"]=self.obj["pos"]+self.obj["vel"]*self.dt

    def update_center_of_gravity(self):
        msum = np.sum(self.obj["mass"])
        cogx = np.sum(self.obj["pos"][:,0]*self.obj["mass"])/msum
        cogy = np.sum(self.obj["pos"][:,1]*self.obj["mass"])/msum
        self.cog = np.array([cogx,cogy])



######################
######################
###  DIAGNOSTICTS  ###
######################
######################
    def print_collisions(self):
        return "No. of planets={:d}".format(self.n)

    def print_stuff(self):
        m   = self.obj["mass"] 
        vx2 = self.obj["vel"][:,0]**2 
        vy2 = self.obj["vel"][:,1]**2
        Ek  = np.sum(0.5*m*(vx2+vy2))
        return "Ek={:.2f} cog=({:.2f},{:.2f}) n={:d}".format(
                Ek,self.cog[0],self.cog[1],self.n)

    def print_energy(self):
        m   = self.obj["mass"] 
        vx2 = self.obj["vel"][:,0]**2 
        vy2 = self.obj["vel"][:,1]**2
        Ek  = np.sum(0.5*m*(vx2+vy2))
        return "Ek={:.2e}".format(Ek)

    def print_diagnostics(self):
        fx  = self.obj["force"][:,0] 
        fy  = self.obj["force"][:,1]
        vx  = self.obj["vel"][:,0] 
        vy  = self.obj["vel"][:,1]
        return "F1=({:.2e} {:.2e})  F2=({:.2e} {:.2e})\n v1=({:.2e} {:.2e})  v2=({:.2e} {:.2e})".format(fx[0],fy[0],fx[1],fy[1],vx[0],vy[0],vx[1],vy[1])

    def print_nothing(self):
        return ""



######################
######################
###    PLOTTING    ###
######################
######################

    def update_plot_objects(self):
        #Save to plot objects
        self.planets.set_offsets(self.obj["pos"])
        self.planets.set_sizes(self.obj["size"])
        self.cogmark.set_offsets(self.cog)
        if self.diagnostic_output:
            self.text.set_text(self.print_collisions())
        if self.follow_center_of_gravity:
            drift = self.cog-self.center
            self.center = self.cog
            self.ax.set_xlim(self.ax.get_xlim()+drift[0])
            self.ax.set_ylim(self.ax.get_ylim()+drift[1])

    def update(self,frame_number):
        if self.exit_at_next_iteration:
            input("STOPPED! Press to exit")
            sys.exit(0)
        self.calculate_forces()
        self.integrate_orbits()
        if self.activate_collisions:
            self.handle_collisions()  
        self.update_center_of_gravity()
        self.update_plot_objects()
        return self.planets,self.text,self.cogmark,

    def start(self):
        self.update_center_of_gravity()

        # Update velocities with a half time shift (LeapFrog Method)
        self.calculate_forces()
        self.obj["vel"]=self.obj["vel"]-self.obj["acc"]*self.dt/2.
        
        #Lag plott-vindu
        self.fig = plt.figure(figsize=(7,7))
        self.ax = plt.axes(xlim=(-self.L,self.L),ylim=(-self.L,self.L))

        #Opprett plotte-objekter
        self.ax.set_title("Tyngdekraft (pythonskole.no)\n"+self.title)
        self.text = self.ax.text(-self.L+0.5,-self.L+0.5,'')
        self.cogmark = self.ax.scatter(self.cog[0],self.cog[1],
                marker='x',c='red')
        self.planets = self.ax.scatter(self.obj["pos"][:,0], 
                self.obj["pos"][:,1], s=self.obj["size"])

        #Start animasjon
        anim = animation.FuncAnimation(self.fig, self.update, 
                interval=self.interval)
        plt.show() 

