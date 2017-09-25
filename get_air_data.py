# get_air_data.py

import os
import requests
import pandas as pd
import sqlalchemy
import datetime
import time
from bs4 import BeautifulSoup as BS

engine = sqlalchemy.create_engine('postgresql://'+os.environ['USERNAME']+':'+os.environ['PASSWORD']+'@'+os.environ['HOSTNAME']+':5432/allergyalert')
today = time.mktime(datetime.datetime.now().timetuple())

url = 'https://www.airnow.gov/index.cfm?action=airnow.local_city&zipcode=37076&submit=Go'
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