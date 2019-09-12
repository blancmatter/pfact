import csv, sys, os, re
import datetime
import numpy as np
import math
from astropy.coordinates import EarthLocation,SkyCoord, AltAz
from astropy.time import Time
from astropy import units as u
from astroplan import Observer, AirmassConstraint, AtNightConstraint, TimeConstraint, is_observable, is_always_observable
from astroplan import download_IERS_A



class tnsVis():
    """
    Object visability methods for calculating airmass, lengths of observable
    time for transient name server objects for different observing locations
    and dates
    """

    def __init__(self, lat, lon, elevation, ra, dec, discDate, airmassConstraint=1.5):
        self.airmassConstraint = airmassConstraint
        self.altConstraint = math.degrees(math.asin(1/self.airmassConstraint))
        self.location = EarthLocation(lat=lat, lon=lon, height=elevation*u.m)
        self.discDate = discDate
        self.observer = Observer(location = self.location, name="LT")
        self.target = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        self.constraints = [AirmassConstraint(self.airmassConstraint), AtNightConstraint.twilight_astronomical()]
        print ("Discovery Date :", discDate.value)


    def time_since_discovery(self):
        """
        Returns astropy Time delta object of time since Discovery to time now
        """
        return Time.now()-self.discDate


    def visible_time(self, date):
        """
        For the evening after the date, specify the visible time within the
        constraintsself.

        Not really working at present
        """


        # Find astronomical times for next night
        darkStart = self.observer.twilight_evening_astronomical(date, which=u'next')
        darkEnd = self.observer.twilight_morning_astronomical(darkStart,which=u'next')

        # Find rise and set times
        riseTime = self.observer.target_rise_time(date, self.target,
        which=u'next', horizon=self.altConstraint*u.deg)
        setTime = self.observer.target_set_time(date, self.target,
        which=u'next', horizon=self.altConstraint*u.deg)

        if (darkStart.value < riseTime.value) and (darkEnd.value > setTime.value):
            print ("During night")
            return setTime-riseTime

        elif (darkStart.value > riseTime.value) and (darkEnd.value > setTime.value):
            print("Darkstart")

        elif (darkStart.value < riseTime.value) and (darkEnd.value < setTime.value):
            print("Darkend")

        elif (darkStart.value > riseTime.value) and (darkEnd.value < setTime.value):
            print("DarkstartandEnd")

        else:
            print("No Constraints matched!!")

    def reportDate(self, name):
        """
        Input ATel name and scrape TNS web page for value using regex
        report the in astropy datetime format??
        """

        # pull html down
        pattern = '\d\d\d\d\w\w\w'

        wget = 'wget -O AT.html https://wis-tns.weizmann.ac.il/object/' + re.findall(pattern, name)[0]
        os.system(wget)

        # Open, read into string and close file and remove file
        textfile = open('AT.html', 'r')
        filetext = textfile.read()
        textfile.close()
        os.system('rm AT.html')

        #find the time_received value
        pattern = re.compile('class=\"cell-time_received\">\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d')
        match = re.findall(pattern, filetext)[0]

        # get down to YYYY-MM-DD HH:MM:SS value
        pattern = '\d\d\d\d\-\d\d-\d\d \d\d:\d\d:\d\d'
        reportDate = re.findall(pattern, match)[0]
        return reportDate

    def reportDelay(self, date):
        """
        Input the report date as an astropy Time object
        return the difference between the discovery and report in units of days
        """
        reportDelay = date - self.discDate
        print ("report : ", date)
        print ("discdate : ", self.discDate)
        print ("report.Delay : ", reportDelay)
        return reportDelay


    def plot(self, date):
        """
        Produce plot of the object visability for date
        Modified from https://docs.astropy.org/en/stable/generated/examples/coordinates/plot_obs-planning.html
        """

        import matplotlib.pyplot as plt
        from astropy.visualization import astropy_mpl_style
        plt.style.use(astropy_mpl_style)

        midnight = self.observer.midnight(date, which='next')
        delta_midnight = np.linspace(-2, 10, 100)*u.hour
        frame_night = AltAz(obstime=midnight+delta_midnight,
                                  location=self.location)
        targetaltazs_night = self.target.transform_to(frame_night)


        ##############################################################################
        # Use  `~astropy.coordinates.get_sun` to find the location of the Sun at 1000


        from astropy.coordinates import get_sun
        delta_midnight = np.linspace(-12, 12, 1000)*u.hour
        times = midnight + delta_midnight
        frame = AltAz(obstime=times, location=self.location)
        sunaltazs = get_sun(times).transform_to(frame)


        ##############################################################################
        # Do the same with `~astropy.coordinates.get_moon` to find when the moon is
        # up. Be aware that this will need to download a 10MB file from the internet
        # to get a precise location of the moon.

        from astropy.coordinates import get_moon
        moon = get_moon(times)
        moonaltazs = moon.transform_to(frame)

        ##############################################################################
        # Find the alt,az coordinates of M33 at those same times:

        targetaltazs = self.target.transform_to(frame)

        ##############################################################################
        # Make a beautiful figure illustrating nighttime and the altitudes of M33 and
        # the Sun over that time:

        plt.plot(delta_midnight, sunaltazs.alt, color='r', label='Sun')
        plt.plot(delta_midnight, moonaltazs.alt, color=[0.75]*3, ls='--', label='Moon')
        plt.scatter(delta_midnight, targetaltazs.alt,
                    c=targetaltazs.az, label='Target', lw=0, s=8,
                    cmap='viridis')
        plt.fill_between(delta_midnight.to('hr').value, 0, 90,
                         sunaltazs.alt < -0*u.deg, color='0.5', zorder=0)
        plt.fill_between(delta_midnight.to('hr').value, 0, 90,
                         sunaltazs.alt < -18*u.deg, color='k', zorder=0)
        plt.hlines(self.altConstraint, -12, 12, colors='red', linestyles='dotted', lw=1)
        plt.colorbar().set_label('Azimuth [deg]')
        plt.legend(loc='upper left')
        plt.xlim(-12, 12)
        plt.xticks(np.arange(13)*2 -12)
        plt.ylim(0, 90)
        plt.xlabel('Hours from Local Midnight')
        plt.ylabel('Altitude [deg]')
        plt.show()


    def get_info(self, date):
        """
        Prints useful info for a given time, for debugging mainly
        Alt - Az of target
        Alt - Az of sun
        Alt - Az of moon
        .....
        """

        return

    def objVis(self):
        """
        Checks if transit is in between twilight hours. If not return error
        Returns the amount of time the object is above given airmass
        """

        objVis = is_observable(self.constraints, self.observer, self.target,
                 time_range=(self.discDate, self.discDate+1*u.day))[0]

        return objVis




def main():
    with open('full.dat') as csvin:

        """
        Header list of TNS csvfile

        headersin = '"ID", \
                   "Name", \
                   "RA", \
                   "DEC", \
                   "Obj. Type", \
                   "Redshift", \
                   "Host Name", \
                   "Host Redshift", \
                   "Discovering Group/s", \
                   "Classifying Group/s", \
                   "Associated Group/s", \
                   "Disc. Internal Name", \
                   "Disc. Instrument/s", \
                   "Class. Instrument/s", \
                   "TNS AT", \
                   "Public", \
                   "End Prop. Period", \
                   "Discovery Mag", \
                   "Discovery Mag Filter", \
                   "Discovery Date (UT)", \
                   "Sender", \
                   "Remarks", \
                   "Ext. catalog/s"'

        headersout =
        """


        reader = csv.DictReader(csvin)


        outtext = []
        header = True
        for row in reader:

            id           = row['ID']
            name         = row['Name']
            ra           = row['RA']
            dec          = row['DEC']
            objType      = row['Obj. Type']
            redshift     = row['Redshift']
            hostname     = row['Host Name']
            hostredshift = row['Host Redshift']
            discDate     = Time.strptime(row['Discovery Date (UT)'], "%Y-%m-%d %H:%M:%S")
            mag          = row['Discovery Mag']
            magFilt      = row['Discovery Mag Filter']

            object=tnsVis(28.762, -17.879, 2363, ra, dec, discDate)


            reportDate = object.reportDate(name)
            reportDelay = object.reportDelay(Time.strptime(reportDate, "%Y-%m-%d %H:%M:%S"))

            row.update({'Vis' : object.objVis()})
            row.update({'Report Date' : object.reportDate(name)})
            row.update({'reportDelay' : reportDelay})
            row.update

            # For first row output column headers
            if header:
                outtext.append(list(row.keys()))
                header =False

            outtext.append(list(row.values()))
            print(row)



    with open('tns_out.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(outtext)




if __name__== "__main__":
    main()
