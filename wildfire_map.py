import sqlite3
import pandas as pd
import folium
from alive_progress import alive_bar

# Connect to SQLite and load data
conn = sqlite3.connect('Data/FPA_FOD_20221014.sqlite')
df = pd.read_sql_query("select * from Fires", conn)
print('Data imported')

# Clean and filter the data
df.drop('Shape', axis=1, inplace=True)
df = df[(df['STATE'] == 'CA') & (df['NWCG_GENERAL_CAUSE'] == 'Arson/incendiarism') & (df['FIRE_YEAR'] == 2020)]

# Extract coordinates and relevant information for popups
coordinates = df[['LATITUDE', 'LONGITUDE']].values.tolist()
popup_info = df[['FIRE_NAME', 'DISCOVERY_DATE', 'FIRE_SIZE']].fillna('Unknown')

# Initialize the map
map = folium.Map(location=[30.55435, -91.03677], zoom_start=6)
fg = folium.FeatureGroup(name='United States')

print('Generating map...')
with alive_bar(len(coordinates)) as bar:
    for coord, info in zip(coordinates, popup_info.itertuples()):
        # Create a dynamic popup string
        popup_content = f"""
        <b>Fire Name:</b> {info.FIRE_NAME}<br>
        <b>Discovery Date:</b> {info.DISCOVERY_DATE}<br>
        <b>Fire Size:</b> {info.FIRE_SIZE} acres
        """
        # Add marker with popup
        fg.add_child(
            folium.Marker(
                location=coord,
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='red')
            )
        )
        bar()

# Add feature group to the map and save
map.add_child(fg)
map.save('Map3.html')
print('Map saved as Map3.html')
