import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from alive_progress import alive_bar

conn = sqlite3.connect('FPA_FOD_20170508.sqlite')
df = pd.read_sql_query("select * from Fires", conn)
print('Data imported')
df.drop('Shape',axis=1, inplace=True)

# df = df[df['FIRE_YEAR']==2006]
df = df[(df['STATE']=='CA') & (df['STAT_CAUSE_DESCR']=='Arson') & (df['FIRE_YEAR']==2015)]

coordinates = df[['LATITUDE','LONGITUDE']].values.tolist()

map = folium.Map(location=[30.55435, -91.03677], zoom_start=6, tiles="Stamen Terrain")
fg = folium.FeatureGroup(name='United States')

print('Generating map...')
with alive_bar(len(coordinates)) as bar:
    for coord in coordinates:
        fg.add_child(folium.Marker(location=coord, popup='What up', icon=folium.Icon(color='red')))
        bar()

map.add_child(fg)
map.save('Map2.html')
