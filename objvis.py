import tnsVis
from astropy.time import Time
from astropy import units as u

time = '2019-08-26 12:37:55'
ra = '21:50:00'
dec = '+10:00:53'

discDate = Time.strptime(time, "%Y-%m-%d %H:%M:%S")

vis = tnsVis.tnsVis(28.762, -17.879, 2363, ra, dec, discDate, airmassConstraint=2)

print(vis.objVis())
diffdate = vis.time_since_discovery()
diffdate.format = 'sec'
print(diffdate.value)
print(vis.visible_time(Time.now()))
vis.plot(Time.now())

# Check if observable
# Check time above airmass 2
