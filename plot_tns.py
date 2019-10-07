import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("tndout2.dat")
data['Discovery Mag'] = pd.to_numeric(data['Discovery Mag'], errors='coerce')
data['reportDelay'] = pd.to_numeric(data['reportDelay'], errors='coerce')

#filtered = data[("Discovery Mag" < 18) & ("Vis" == "True") & ("reportDelay" < 5)]

filter = data["Vis"] == "True"
data.where(filter, inplace=True)

filter = data["Discovery Mag"] < 22
data.where(filter, inplace=True)

filter = data["reportDelay"] < 6
data.where(filter, inplace=True)



#fig = px.histogram(data, x="Discovery Mag", hover_data=data.columns)
fig = go.Figure(data=[go.Histogram(x=data["Discovery Mag"], cumulative_enabled=False)])
fig.update_xaxes(title_text='Report Delay in days')
fig.update_yaxes(title_text='Number')
fig.update_layout(
    title=go.layout.Title(
        text="Plot Title",
        xref="paper",
        x=0
    ))
fig.show()
