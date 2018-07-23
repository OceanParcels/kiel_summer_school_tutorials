import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

class ParticleData(object):
    def __init__(self, pfile):
        dataset = Dataset(pfile)
        self.id = dataset.variables['trajectory'][:]
        self.time = dataset.variables['time'][:]
        self.lon = dataset.variables['lon'][:]
        self.lat = dataset.variables['lat'][:]
        dataset.close()

    def keepParticles(self, pind):
        self.lon = p.lon[pind,:]
        self.lat = p.lat[pind,:]
        self.id = p.id[pind,:]
        self.time = p.time[pind,:]

pfile = './nemo.nc'
p = ParticleData(pfile)
print('Total number of particles: %d' % p.lon.shape[0])

pland = np.logical_and(abs(p.lon[:,0]-p.lon[:,-1]) < 1e-4, abs(p.lat[:,0]-p.lat[:,-1]) < 1e-4)
pind = np.where(np.logical_not(pland))[0]
p.keepParticles(pind)
wetParticles = p.lon.shape[0]
print('Number of initially wet particles: %d' % wetParticles)


plt.figure(num=None)
m = Basemap(projection='cass', lon_0=4, lat_0=55, llcrnrlat=40, urcrnrlat=60, llcrnrlon=-5, urcrnrlon=10, resolution='i')
m.drawcoastlines()
m.drawparallels(np.arange(-90, 91, 3), labels=[True, False, False, False])
m.drawmeridians(np.arange(-180, 181, 3), labels=[False, False, False, True])
#m.fillcontinents(color='blanchedalmond')
m.drawmapboundary(fill_color='aliceblue')



day = -1
xs, ys = m(p.lon[:,day], p.lat[:,day])
m.scatter(xs, ys, c=p.id[:,day], s=1)
plt.show()
