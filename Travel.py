import pandas as pd
import altair as alt
import streamlit as st
from vega_datasets import data

#import cities in US and their Lat/Long
cities = pd.read_excel('uscities.xlsx')
#import recorded visited cities
visited = pd.read_excel('https://docs.google.com/spreadsheets/d/e/2PACX-1vQwWC_DUgPtplFGaqPOFOwj4Z0TA_83iJuwf2Bq6XF1O6VkRwWkqBdA7uq2kNu6MILOpqfkLJj3CCSX/pub?output=xlsx')

#clean visited cities data
visited['city'] = visited['What City Did You Visit?']
visited['state_id'] = visited['What State? (Abbreviated)']

citylist = visited[["What City Did You Visit?","What State? (Abbreviated)"]]

#clean cities information data
citiesfiltered = cities[["city","state_id", "lat", "lng"]]

#combine useful data
final = pd.merge(visited, citiesfiltered)

states = alt.topo_feature(data.us_10m.url, feature='states')
points = alt.Chart(final).mark_circle().encode(
    longitude='lng',
    latitude='lat',
    size=alt.value(25),
    tooltip='city'
)
background = alt.Chart(states).mark_geoshape(
    fill='lightgrey',
    stroke='black'
).project('albersUsa').properties(
    width=1000,
    height=600
)

st.header("A visual of visited Cities")
st.subheader("The Map:")
st.write(background + points)

st.subheader("The list of Cities:")
st.dataframe(citylist)

with st.expander("Credits"):
    st.write("Made by Sam Carlson: https://github.com/samuelrcarlson")
    st.write("Made possible using https://simplemaps.com/data/us-cities")
