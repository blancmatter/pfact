import csv, sys
import datetime
import numpy as np
from astropy.coordinates import EarthLocation,SkyCoord, AltAz
from astropy.time import Time
from astropy import units as u
from astroplan import Observer, AirmassConstraint, AtNightConstraint, TimeConstraint, is_observable, is_always_observable



class tnsVis():
    """
    Object visability methods for calculating airmass, lengths of observable time for transient name server objects for different observing locations and dates
    """

    def __init__(self, lat, lon, elevation, ra, dec, date):
        self.location = EarthLocation(lat=lat, lon=lon, height=elevation*u.m)
        self.date = date
        self.observer = Observer(location = self.location, name="LT")
        self.target = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        self.constraints = [AirmassConstraint(1.5), AtNightConstraint.twilight_astronomical()]




    def getDark(self, date):
        """
        Returns the start and end of astronomical dark time,
        for a given date. Dark time is defined as the time that the sun is -18 degrees below the horizon

        Uses the astroplan

        @param  date
        @return list - [startDate, endDate]
        """

        t_eve = self.observer.twilight_evening_astronomical(date, which=u'next')
        t_morn = self.observer.twilight_morning_astronomical(date,which=u'next')

        return (t_eve, t_morn)


    def objVis(self):
        """
        Checks if transit is in between twilight hours. If not return error
        Returns the amount of time the object is above given airmass
        """

        objVis = is_observable(self.constraints, self.LT, self.target, time_range=(self.date, self.date+1*u.day))

        return objVis




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

            object=tnsVis(28.762, -17.879, 2363, ra, dec, discDate)

            print(ra, dec)
            print(row['Discovery Date (UT)'])
            print(object.getDark(discDate))
            print(object.objVis(2, discDate))
            exit()

if __name__== "__main__":
    main()
