import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
mags = []
delay = []
"""
with open('tns_out.csv') as csvin:
    reader = csv.DictReader(csvin)
    for row in reader:
        if 'True' in row['Vis']:
            mags.append(row['Discovery Mag'])
            delay.append(row['reportDelay'])


print (len(mags))
print (len(delay))
plt.hist(mags, density=False, bins=10)
plt.ylabel('Number');
plt.show()
"""
data = pd.read_csv("tns_out.csv")
data['Discovery Mag'] = pd.to_numeric(data['Discovery Mag'], errors='coerce')
data['reportDelay'] = pd.to_numeric(data['reportDelay'], errors='coerce')

#filtered = data[("Discovery Mag" < 18) & ("Vis" == "True") & ("reportDelay" < 5)]

filter = data["Vis"] == "True"
data.where(filter, inplace=True)

filter = data["Discovery Mag"] < 20
data.where(filter, inplace=True)

filter = data["reportDelay"] < 5
data.where(filter, inplace=True)

print (len(data.index))

tips = px.data.tips()
fig = px.histogram(data, x="Discovery Mag", hover_data=data.columns)
fig.show()
