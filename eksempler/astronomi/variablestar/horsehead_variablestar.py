import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
plt.style.use(astropy_mpl_style)
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits

image_file = get_pkg_data_filename('tutorials/FITS-images/HorseHead.fits')

fits.info(image_file)
image_data = fits.getdata(image_file,ext=0)

print(image_data.shape)

#print(image_data[0][:])

#plt.imshow(image_data,cmap='gray')
#plt.colorbar()
#plt.show()

#print(range(193,208)

#for i in range(193,208):
#    print(i)
#    plt.plot(image_data[i][:])
#plt.show()

def crop(data,x,y,d=10):
    return data[x-d:x+d,y-d:y+d]

star = crop(image_data,200,277)
background = crop(image_data,130,150)

flux = np.sum(star)
dark = np.sum(background)
rel_flux = flux-dark
print("Relative flux:",rel_flux)

print(np.sum(star))
plt.imshow(star,cmap='gray')
plt.colorbar()
plt.show()






#local_file = 'CPVelV-band/lsc1m005-kb78-20160219-0152-e90_crop.fits'
#hdul = fits.open(local_file)
#hdul.info()

