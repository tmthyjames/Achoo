# get_allergy_data.py

import datetime
import os
import requests
import time

import pandas as pd
import sqlalchemy


# get forecast
# url = "https://www.pollen.com/api/forecast/extended/pollen/37076"
# get 30 day history
# url = 'https://www.pollen.com/api/forecast/historic/pollen/37076/30'

engine = sqlalchemy.create_engine('postgresql://' + os.environ['USERNAME'] + ':' + os.environ['PASSWORD'] + '@' + os.environ['HOSTNAME'] + ':5432/allergyalert')
url = "https://www.pollen.com/api/forecast/current/pollen/" + os.environ['POLLEN_ZIPCODE']
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

for n, row in enumerate(allergens):
    allergens[n]['Triggers'] = ', '.join([i['Name'] for i in allergens[n]['Triggers']])
    allergens[n]['dateof'] = today

allergens_df = pd.DataFrame(allergens)

allergens_df.to_sql('allergens', con=engine, if_exists='append', index=False)
