#!/usr/bin/python3

import os, sys

command = 'wget -O PAGE.csv "https://wis-tns.weizmann.ac.il/search?&page=PAGE&num_page=1000&discovered_period_value=12&discovered_period_units=months&format=csv"'

for i in range(1,16):
    #print(command.replace('PAGE', str(i)))
    #os.system(command.replace('PAGE', str(i)))

    command = 'tail -n +1 ' + str(i) + '.csv >> full.csv'
    print (command)
    os.system(command)
