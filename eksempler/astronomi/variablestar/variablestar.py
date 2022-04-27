from os import listdir
from os.path import isfile, join

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename
plt.style.use(astropy_mpl_style)


class Frame:
    def __init__(self,x,y,d=10,label='',data=None):
        self.x = x
        self.y = y
        self.d = d
        self.data = data
        self.label = label
        self.xframe = [x-d,x-d,x+d,x+d,x-d]
        self.yframe = [y-d,y+d,y+d,y-d,y-d]
    
    def crop(self,data):
        x = self.x
        y = self.y
        d = self.d
        return data[y-d:y+d,x-d:x+d]

    def flux(self,data):
        x = self.x
        y = self.y
        d = self.d
        return np.max(data[y-d:y+d,x-d:x+d])

    def plotframe(self,style='r-'):
        plt.plot(self.xframe,self.yframe,style)

def crop(data,x,y,d=10):
    return data[y-d:y+d,x-d:x+d]

def cropframe(x,y,d=10):
    xframe = [x-d,x-d,x+d,x+d,x-d]
    yframe = [y-d,y+d,y+d,y-d,y-d]
    return xframe,yframe

path = 'CPVel-Vband'
fitsfiles = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
print(len(fitsfiles))
print(fitsfiles)

for fits_file in fitsfiles:
    #fits_file = 'CPVelV-band/lsc1m005-kb78-20160219-0152-e90_crop.fits'
    image_data = fits.getdata(fits_file,ext=0)

    print("Fits file:",fits_file)
    print("Image size:",image_data.shape)

    star = Frame(663,675,20,'Star')
    star_image = star.crop(image_data)
    star_flux = star.flux(image_data)
    dark = Frame(700,500,20,'Dark')
    dark_image = dark.crop(image_data)
    dark_flux = dark.flux(image_data)
    rel_flux = star_flux-dark_flux

    print("Star flux: ",star_flux)
    print("Background flux: ",dark_flux)
    print("Relative flux:",rel_flux)
    print("SN ratio:",(star_flux-dark_flux) / dark_flux)
    print()


    if True:
        plt.imshow(image_data,cmap='gray',norm=LogNorm())
        star.plotframe('r-')
        dark.plotframe('b-')
        plt.colorbar()
        plt.show()

        plt.imshow(star_image,cmap='gray',norm=LogNorm())
        plt.title("Star")
        plt.colorbar()
        plt.show()

        plt.imshow(dark_image,cmap='gray',norm=LogNorm())
        plt.title("Dark")
        plt.colorbar()
        plt.show()

        #for i in range(image_data.shape[0]):
        #    plt.plot(image_data[i][:])
        #plt.yscale('log')
        #plt.show()

    a = input("Done?")


#LIbrary: https://stak-notebooks.readthedocs.io/_/downloads/en/latest/pdf/
#Image analysis: OpenCV
