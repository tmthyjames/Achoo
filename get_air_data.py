# get_air_data.py

import pandas as pd

import constants as const
import utils


engine = utils.get_db_engine()
today = utils.get_current_time()

soup = utils.get_uri_content(uri=const.AIRNOW_URI,
                             content_type='html')

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
