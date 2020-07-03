import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# header
st.title("London Bikes")
st.subheader("Number of Trips starting from Hyde Parker Corner")

# read data - source: London Bicycle Hires from Greater London Authority on Google Datasets via Bigquery
df = pd.read_csv('london_bikes.csv')

# area plot
df['start_day'] = pd.to_datetime(df['start_date']).dt.date
df['start_wod'] = pd.to_datetime(df['start_date']).dt.weekday_name
df_trips_by_day = df['start_day'].value_counts()
st.area_chart(df_trips_by_day)

# arc plot
df_end_station = df[['start_latitude', 'start_longitude', 'end_latitude', 'end_longitude',
                     'trip_dist']]

midpoint = (np.average(df_end_station["end_latitude"]),
            np.average(df_end_station["end_longitude"]))


st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ArcLayer",
            data=df_end_station,
            get_source_position="[start_longitude, start_latitude]",
            get_target_position="[end_longitude, end_latitude]",
            get_source_color=[0, 30, 87, 160],
            get_target_color=[0, 30, 190, 160]

        )
    ]
))