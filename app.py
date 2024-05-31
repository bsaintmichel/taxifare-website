import streamlit as st
import requests
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(layout="wide")

'''
# My taxi disruption app

## Please input your details here
'''

default_coords = [40.758889, -73.959167]
default_address = '30, Rockefeller Plaza, New York'

m = folium.Map(location=default_coords, zoom_start=13, width=1200, height=600)
client = Nominatim(user_agent='TaxiFare')
icon_p=folium.Icon(color='blue')
icon_d=folium.Icon(color='red')

col1, col2 = st.columns(2)
time = col1.time_input('Time Input')
date = col2.date_input('Date Input')
pickup_location = col1.text_input('Pickup Location', value=default_address)
dropoff_location = col2.text_input('Dropoff Location', value=default_address)
passenger_num = st.slider('Passengers', min_value=1, max_value=8)


geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
dropoff_exact =  geolocator.geocode(dropoff_location)
pickup_exact = geolocator.geocode(pickup_location)

dropoff_gps = [dropoff_exact.latitude, dropoff_exact.longitude]
pickup_gps = [pickup_exact.latitude, pickup_exact.longitude]

folium.Marker(pickup_gps, tooltip='Pickup Point', icon=icon_p).add_to(m)
folium.Marker(dropoff_gps, tooltip='Dropoff Point', icon=icon_d).add_to(m)


st_folium(m, width=1200, height=600)

'''
## Fare
'''

url = 'https://taxifare-wfibpwbfra-ew.a.run.app/predict'

params = {'pickup_datetime': datetime.combine(date, time),
          'pickup_longitude': pickup_gps[1],
          'pickup_latitude': pickup_gps[0],
          'dropoff_longitude': dropoff_gps[1],
          'dropoff_latitude': dropoff_gps[0],
          'passenger_count': passenger_num}

with st.spinner(text='Working ...'):
    fare = requests.get(url, params = params).json()

st.metric(label="You will pay", value=f"${fare['fare']:.2f}")


'''
### Change theme
'''

color = st.color_picker('Pick a color', value='#FFFFFF')
custom_str = f'background-color : {color};'
my_str = '<style> \n body { \n ' + custom_str + ' \n } \n '
my_str_2 = '.st-emotion-cache-1jicfl2{ ' + custom_str + '\n } \n </style>'
st.markdown(my_str + my_str_2, unsafe_allow_html=True)

st.code(my_str + my_str_2, language='html')


if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
