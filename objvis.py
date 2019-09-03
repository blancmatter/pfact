import tnsVis
from astropy.time import Time
from astropy import units as u

time = '2019-08-26 12:37:55'
ra = '22:31:29'
dec = '+16:13:53'

discDate = Time.strptime(time, "%Y-%m-%d %H:%M:%S")

vis = tnsVis.tnsVis(28.762, -17.879, 2363, ra, dec, discDate)

print (vis.objVis())


# Check if observable
# Check time above airmass 2
