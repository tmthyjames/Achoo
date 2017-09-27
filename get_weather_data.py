# get_weather_data.py

import datetime
import os
import requests
import time

import pandas as pd
import sqlalchemy


engine = sqlalchemy.create_engine('postgresql://' + os.environ['USERNAME'] + ':' + os.environ['PASSWORD'] + '@' + os.environ['HOSTNAME'] + ':5432/allergyalert')
today = time.mktime(datetime.datetime.now().timetuple())

url = 'https://api.darksky.net/forecast/' + os.environ['DARK_SKY_API_KEY'] + '/' + os.environ['DARK_SKY_LOCATION']
req = requests.get(url)
resp = req.json()

for key in resp.keys():
    if isinstance(resp.get(key), dict) and 'data' in resp.get(key):
        for n, i in enumerate(resp.get(key)['data']):
            resp.get(key)['data'][n]['currentTime'] = today

resp['currently']['lat'] = resp['latitude']
resp['currently']['lng'] = resp['longitude']

current_df = pd.DataFrame([resp['currently']])
daily_df = pd.DataFrame(resp['daily']['data'])
hourly_df = pd.DataFrame(resp['hourly']['data'])
minutely_df = pd.DataFrame(resp['minutely']['data'])

tables = ['current_weather', 'daily_weather', 'hourly_weather', 'minutely_weather']
for table in tables:
    daily_df.to_sql(table, con=engine, if_exists='append', index=False)
