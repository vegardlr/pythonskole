import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

image_file = get_pkg_data_filename('tutorials/FITS-images/HorseHead.fits')
fits.info(image_file)
image_data = fits.getdata(image_file,ext=0)

def crop(data,x,y,d=10):
    return data[x-d:x+d,y-d:y+d]

vmin = 6000
vmax = 20000

plt.imshow(image_data,cmap='gray',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.grid(False)
plt.show()

star       = crop(image_data,200,277)
background = crop(image_data,130,150)

flux = np.sum(star)
dark = np.sum(background)
rel_flux = flux-dark
print("Relative flux:",rel_flux)

print("Sum star:",np.sum(star))
plt.imshow(star,cmap='gray',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.grid(False)
plt.show()

print("Sum background:",np.sum(background))
plt.imshow(background, cmap='gray',vmin=vmin,vmax=vmax)
plt.colorbar()
plt.grid(False)
plt.show()

