###   Pythonskole.no    Tyngdekraft    ###
### 23.11.2021  kontakt@pythonskole.no ###
### Beta-versjon 
### Planlagte oppgraderinger: 
###  - Endre struktur til bibliotek (import Tyngdekraft)
###  - Teste og reaktivere kollisjoner

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import animation

######################
######################
### INITIALIZATION ###
######################
######################

class Orbit():
	def __init__(self,dt=0.03,L=20.0):
		self.tstep = 0
		self.dt = dt
		self.n = 0
		self.L = L
		self.interval=10
		self.origo = np.array([L/2.,L/2.])
		self.cog = self.origo


	def addObject(self,pos,vel,size):
		datatype = np.dtype([
			('pos', np.float64 , 2),('vel', np.float64 , 2),
			('acc', np.float64 , 2),('force', np.float64 , 2),
			('mass', np.float64 , 1),('size', np.float64 , 1)])
		mass = size**2
		force = np.zeros(2)
		new = np.zeros(1,dtype=datatype) 
		new["pos"] = pos
		new["vel"] = vel
		new["acc"] = np.zeros(2)
		new["force"] = np.zeros(2)
		new["mass"] = mass
		new["size"] = size
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

	def initialize(self):
		self.find_center_of_gravity()
		# Update velocotues with a half time shift (LeapFrog Method)
		self.calculate_forces()
		self.obj["vel"]=self.obj["vel"]-self.obj["acc"]*self.dt/2.

	def calculate_forces(self,mode='std'):
		# Use linear algebra to calculate the forces acting 
		# between each and every planet in the simulation, 
		# using the N-body method. 
		gravity_factor = 0.0005
		ones = np.ones(self.n)
		# Get mass and positions of planets
		m = self.obj["mass"][:]
		x = self.obj["pos"][:,0]
		y = self.obj["pos"][:,1]
		# Calculate discances between each particle and product of masses
		dx = np.outer(ones,x) - np.outer(x,ones)
		dy = np.outer(ones,y) - np.outer(y,ones)
		m2 = np.outer(ones,m) * np.outer(m,ones)
		d2 = dx**2 + dy**2
		np.fill_diagonal(d2,np.inf)
		# Calculate gravity, angle between positions, and force components
		f  = gravity_factor*m2/d2
		theta = np.arctan2(dy, dx)
		fx = np.sum(f * np.cos(theta),1)
		fy = np.sum(f * np.sin(theta),1)
		#Save force and acceleration acting on each planet
		self.obj["force"] = np.transpose(np.vstack((fx,fy)))
		self.obj["acc"]   = np.transpose(np.vstack((fx/m,fy/m)))

#Collisions module need more work before it is safe to use
#It is per now deactivated (in function update())
	def handle_collisions(self):
		size_factor = 0.004
		ones = np.ones(self.n)
		# Get positions of all the planets
		x = self.obj["pos"][:,0]
		y = self.obj["pos"][:,1]
		# Calculate discances between each planet
		dx = np.outer(ones,x) - np.outer(x,ones)
		dy = np.outer(ones,y) - np.outer(y,ones)
		d2 = dx**2 + dy**2
		np.fill_diagonal(d2,np.inf)
		# Is their size larger than their distance?
		s = self.obj["size"][:]
		s2 = size_factor**2 * (np.outer(ones,s) + np.outer(s,ones))**2
		# Count all planets that has collided
		collisions = np.tril(d2 <= s2)
		deletelist = []
		if np.sum(collisions) > 0:
			indices = np.column_stack(np.where(collisions))
			for ind in indices:
				self.collision(ind)
				deletelist.append(ind[1])
			for i in deletelist: 
				self.obj = np.delete(self.obj,i)
			self.n = len(self.obj)

                

	def collision(self,i):
		msum = np.sum(self.obj["mass"][i])
		psum = np.sum(self.obj["vel"][i]*self.obj["mass"][i],0)
		if self.obj["mass"][i[0]] < self.obj["mass"][i[1]]:
			i = np.flip(i,0)
		self.obj["mass"][i[0]] = msum
		self.obj["size"][i[0]] = np.sqrt(np.sum(self.obj["size"][i]**2))
		#self.obj["vel"][i[0],:] =  psum / msum
		self.obj["force"][i[0],:] = np.zeros(2)
		self.obj["acc"][i[0],:] = np.zeros(2)
		#self.obj["size"][i[1]] = 0.0
		#self.obj = np.delete(self.obj,i[1])

	def integrate_orbits(self):
		if self.n == 0:
			raise ValueError('No more objects')

		self.tstep += 1
		self.obj["vel"]=self.obj["vel"]+self.obj["acc"]*self.dt
		self.obj["pos"]=self.obj["pos"]+self.obj["vel"]*self.dt

	def find_center_of_gravity(self):
		msum = np.sum(self.obj["mass"])
		cogx = np.sum(self.obj["pos"][:,0]*self.obj["mass"])/msum
		cogy = np.sum(self.obj["pos"][:,1]*self.obj["mass"])/msum
		self.cog = np.array([cogx,cogy])



######################
######################
###  DIAGNOSTICTS  ###
######################
######################
	def print_url(self):
		return "pythonskole.no/koder/astronomi/tyngdekraft"

	def print_number(self):
		return "No. of planets={:d}".format(self.n)

	def print_stuff(self):
		m   = self.obj["mass"] 
		vx2 = self.obj["vel"][:,0]**2 
		vy2 = self.obj["vel"][:,1]**2
		Ek  = np.sum(0.5*m*(vx2+vy2))
		return "Ek={:.2f} cog=({:.2f},{:.2f}) n={:d}".format(Ek,self.cog[0],self.cog[1],self.n)

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

	def print_title(self):
		#return self.print_url()
		return "Pythonskole.no - Tyngdekraft"



######################
######################
###    PLOTTING    ###
######################
######################

	def update_plot_objects(self):
		#Save to plot objects
		self.planets.set_offsets(self.obj["pos"])
		self.planets.set_sizes(self.obj["size"])
		self.text.set_text(self.print_nothing())
		self.cogmark.set_offsets(self.cog)
		offset = self.cog - self.origo
		self.ax.set_xlim(self.ax.get_xlim()+offset[0])
		self.ax.set_ylim(self.ax.get_ylim()+offset[1])
		self.ax.set_title(self.print_title())
		self.origo = self.cog

	def update(self,frame_number):
		self.calculate_forces()
		self.integrate_orbits()
		##self.handle_collisions()  
		self.find_center_of_gravity()
		self.update_plot_objects()
		return self.planets,self.text,self.cogmark,

	def run(self):
		self.fig = plt.figure(figsize=(7,7))
		self.ax = plt.axes(xlim=(0,self.L),ylim=(0,self.L))
		self.text = self.ax.text(0.5,0.5,'')
		self.cogmark = self.ax.scatter(self.cog[0],self.cog[1],
				marker='x',c='red')
		self.planets = self.ax.scatter(self.obj["pos"][:,0], 
				self.obj["pos"][:,1], s=self.obj["size"])
		anim = animation.FuncAnimation(self.fig, self.update, 
				interval=self.interval)
		plt.show() 





# SIMULERING MED TYNGDEKRAFT I PYTHON
# KJØRT PÅ EN HELT VANLIG LAPTOP :)
# Pythonskole.no 23.11.2021
# Beta-versjon
if __name__ == "__main__":
	#Set up simulation domain
	orbits = Orbit(L=20.0)
	#Add three large objects
	orbits.addObject(orbits.origo,[0,0],200.)
	orbits.addObject(orbits.origo+[-2.0,0],[0,3.0],30.)
	orbits.addObject(orbits.origo+[+2.0,0],[0,-3.0],30.)
	#Add 100 small objects
	L = orbits.L
	for i in range(10):
		r = np.random.uniform(0.1*L,0.5*L)
		mass = np.random.uniform(1.0,1.5)
		v = 7.0*mass/r
		theta = np.random.uniform(0.0,2.0*np.pi)
		pos = np.array([r*np.cos(theta),r*np.sin(theta)])+orbits.origo
		vel = np.array([v*np.sin(theta),-v*np.cos(theta)])
		orbits.addObject(pos,vel,mass)

	#Initialize and start code
	orbits.initialize()
	orbits.run()


