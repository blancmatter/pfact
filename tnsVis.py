import csv
import datetime
from astropy.coordinates import EarthLocation,SkyCoord, AltAz
from astropy.time import Time
from astropy import units as u
from astroplan import Observer



class tnsVis():
    """
    Object visability methods for calculating airmass, lengths of observable time for transient name server objects for different observing locations and dates
    """

    def __init__(self, lat, lon, alt, ra, dec):
        self.location = EarthLocation(lat=lat, lon=lon, height=alt*u.m)
        self.LT = Observer (location = self.location, name="LT")
        self.coord = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        return



    def getDark(self, date):
        """
        Returns the start and end of astronomical dark time,
        for a given date. Dark time is defined as the time that the sun is -18 degrees below the horizon

        Uses the astroplan

        @param  date
        @return list - [startDate, endDate]
        """

        t_eve = self.LT.twilight_evening_astronomical(date, which=u'nearest')
        t_morn = self.LT.twilight_morning_astronomical(date, which=u'nearest')

        return (self.LT.astropy_time_to_datetime(t_eve), self.LT.astropy_time_to_datetime(t_morn))




    def obsTime(ra, dec, date, airmass, self):
        """
        Return the highest airmass observable for the object and time above a
        specified airmass for a specific night
        """






        return




def main():
    with open('tns_search.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['ID'], row['RA'], row['DEC'], row['Discovery Date (UT)'],row['Discovery Mag'], row['Discovery Mag Filter'])


            id       = row['ID']
            name     = row['Name']
            objType  = row['Obj. Type']
            discDate = Time.strptime(row['Discovery Date (UT)'], "%Y-%m-%d %H:%M:%S")
            ra       = row['RA']
            dec      = row['DEC']
            mag      = row['Discovery Mag']
            magFilt  = row['Discovery Mag Filter']

            object=tnsVis(28.762, -17.879, 2363, ra, dec)


            print(object.getDark(discDate))
            exit()

if __name__== "__main__":
    main()
