import csv


with open('tns_search.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['ID'], row['RA'], row['DEC'], row['Discovery Date (UT)'])
