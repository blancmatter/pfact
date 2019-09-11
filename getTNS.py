#!/usr/bin/python3
"""
Script to pull all historical data from TNS for one year and concatenate
into a single full.cat casv file
"""

import os, sys

DRYRUN = 1 # turn off to actually trigger actions
command = 'wget -O PAGE.csv "https://wis-tns.weizmann.ac.il/search?&page=PAGE&num_page=1000&discovered_period_value=12&discovered_period_units=months&format=csv"'

for i in range(1,16):


    if i == 1:
        catcom = 'cat 1.csv > full.csv'
    else:
            catcom = 'tail -n +1 ' + str(i) + '.csv >> full.cat'

    print(command.replace('PAGE', str(i)))
    print (catcom)

    if DRYRUN == False:
        os.system(command.replace('PAGE', str(i)))
        os.system(catcom)
        os.system('rm -r *.csv')
