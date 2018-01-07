import os
import requests
import pandas as pd
import sqlalchemy
import time
import datetime
from bs4 import BeautifulSoup as BS

engine = sqlalchemy.create_engine('postgresql://tdobbins:1q2w3e4r5t6y@localhost:5432/achoo')
today = time.mktime(datetime.datetime.now().timetuple())

users = engine.execute('select distinct on (zipcode) * from users ').fetchall()

def get_weather_data(lat, lng):
    url = 'https://api.darksky.net/forecast/c9cbc2214a572195e26faa8664e3d052/'+str(lat)+','+str(lng)
    req = requests.get(url)
    resp = req.json()

    for key in resp.keys():
        if isinstance(resp.get(key), dict) and 'data' in resp.get(key):
            for n,i in enumerate(resp.get(key)['data']):
                resp.get(key)['data'][n]['currentTime'] = today

    resp['currently']['lat'] = resp['latitude']
    resp['currently']['lng'] = resp['longitude']

    current_df = pd.DataFrame([resp['currently']])
    daily_df = pd.DataFrame(resp['daily']['data'])
    hourly_df = pd.DataFrame(resp['hourly']['data'])
    minutely_df = pd.DataFrame(resp['minutely']['data'])

    current_columns = ['apparentTemperature', 'cloudCover', 'dewPoint', 'humidity', 'icon', 'lat', 'lng', 'nearestStormBearing', 'nearestStormDistance', 'ozone', 'precipIntensity', 'precipProbability', 'pressure', 'summary', 'temperature', 'time', 'uvIndex', 'visibility', 'windBearing', 'windGust', 'windSpeed']
    for i in current_df.columns:
        if i not in current_columns:
            del current_df[i]

    hourly_columns = [u'apparentTemperature', u'cloudCover', u'currentTime', u'dewPoint', u'humidity', u'icon', u'ozone', u'precipIntensity', u'precipProbability', u'precipType', u'pressure', u'summary', u'temperature', u'time', u'uvIndex', u'visibility', u'windBearing', u'windGust', u'windSpeed']
    for i in hourly_df.columns:
        if i not in hourly_columns:
            del hourly_df[i]

    tables = ['current_weather', 'daily_weather', 'hourly_weather', 'minutely_weather']
    data_to_import = [current_df, daily_df, hourly_df, minutely_df]
    for data, table in zip(data_to_import, tables):
        data.to_sql(table, con=engine, if_exists='append', index=False)
        
    return None

def get_allergen_data(zipcode):
    # get forecast
    # url = "https://www.pollen.com/api/forecast/extended/pollen/37076"
    # get 30 day history
    # url = 'https://www.pollen.com/api/forecast/historic/pollen/37076/30'

    url = "https://www.pollen.com/api/forecast/current/pollen/" + "37122"
    today = time.mktime(datetime.datetime.now().timetuple())

    headers = {
        'accept': "application/json, text/plain, */*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.8,it;q=0.6",
        'connection': "keep-alive",
        'cookie': "ASP.NET_SessionId=udv21cgxl23lrxupoxt5eowg; geo=37076; __RequestVerificationToken=WNDbD03-8Abz7c7XERainKA6bQpRKizwCgCNLLpzxW5ALMV7MMTTOob2wTbI9q2UIwuDJOR68xz084_DBlRKN3EYfJ1vedX2M63WyCZXnzM1; _gat=1; _ga=GA1.2.1454068007.1505789851; _gid=GA1.2.1546508119.1505789851; session_depth=www.pollen.com%3D3%7C668625674%3D3",
        'host': "www.pollen.com",
        'referer': "https://www.pollen.com/forecast/current/pollen/37076",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)

    resp = response.json()

    allergens = resp['Location']['periods']

    for n,row in enumerate(allergens):
        allergens[n]['Triggers'] = ', '.join([i['Name'] for i in allergens[n]['Triggers']])
        allergens[n]['dateof'] = today

    allergens_df = pd.DataFrame(allergens)

    allergens_df.to_sql('allergens', con=engine, if_exists='append', index=False)
    
    return None

def get_airquality_data(zipcode):

    today = time.mktime(datetime.datetime.now().timetuple())

    url = 'https://www.airnow.gov/index.cfm?action=airnow.local_city&zipcode=37122&submit=Go'
    resp = requests.get(url)
    soup = BS(resp.content, 'html')

    aqi_table = soup.find_all('table', {'width': '65%'})[0]

    rows = []
    for table_row in aqi_table.find_all('tr'):
        pollutant = table_row.find_all('td', {'class': 'AQDataPollDetails'})[0].text.strip()
        value = table_row.find_all('td', {'height': '27'})[0].text.strip()
        row = {
            'pollutant': pollutant,
            'value': value,
            'dateof': today
        }
        rows.append(row)

    pollutant_df = pd.DataFrame(rows)
    pollutant_df.to_sql('pollutants', con=engine, if_exists='append', index=False)
    
    return None

for user in users:
    get_weather_data(user.lat, user.lng)
    get_allergen_data(user.zipcode)
    get_airquality_data(user.zipcode)