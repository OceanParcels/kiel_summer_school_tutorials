from parcels import FieldSet, AdvectionRK4, ParticleFile, ParticleSet, JITParticle
from parcels import ErrorCode
import numpy as np
from glob import glob
from parcels import timer
import time as timelib


def get_nemo_fieldset():
    data_dir = '/Users/delandmeter/data/NEMO-MEDUSA/NorthSea/ORCA025-N006/'
    ufiles = sorted(glob(data_dir+'means/ORCA025-N06_2000????d05U.nc'))
    vfiles = sorted(glob(data_dir+'means/ORCA025-N06_2000????d05V.nc'))
    mesh_mask = data_dir + 'domain/coordinates.nc'

    filenames = {'U': ufiles,
                 'V': vfiles,
                 'mesh_mask': mesh_mask}

    variables = {'U': 'uos',
                 'V': 'vos'}
    dimensions = {'lon': 'glamf', 'lat': 'gphif', 'time': 'time_counter'}
    field_set = FieldSet.from_nemo(filenames, variables, dimensions)
    return field_set


def DeleteParticle(particle, fieldset, time, dt):
    particle.delete()


timer.root = timer.Timer('Main')
timer.fieldset = timer.Timer('FieldSet', parent=timer.root)
field_set = get_nemo_fieldset()
timer.fieldset.stop()

kernel = AdvectionRK4

time0 = field_set.U.grid.time[0]
lonv = np.arange(-6,10.1,.2)
latv = np.arange(50,63,.2)
lon, lat = np.meshgrid(lonv, latv)
lon = lon.flatten()
lat = lat.flatten()
time = time0 * np.ones(lon.shape)
pset = ParticleSet.from_list(field_set, JITParticle, lon=lon, lat=lat, time=time)
kernel = AdvectionRK4
timer.particlefile = timer.Timer('ParticleFile', parent=timer.root)
outfile = __file__[:-3]
pfile = ParticleFile(outfile, pset)
pfile.write(pset, pset[0].time)
timer.particlefile.stop()
tic = timelib.time()
ndays = 60
timer.run = timer.Timer('Execution', parent=timer.root, start=False)
for d in range(ndays):
    print('running %d / %d: time %g' % (d+1, ndays, timelib.time()-tic))
    timer.run.start()
    pset.execute(kernel, runtime=86400, dt=900)#, recovery={ErrorCode.ErrorOutOfBounds: DeleteParticle})
    timer.run.stop()
    timer.particlefile.start()
    pfile.write(pset, pset[0].time)
    timer.particlefile.stop()

timer.root.stop()
timer.root.print_tree()

