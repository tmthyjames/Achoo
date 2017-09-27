# get_weather_data.py

import pandas as pd

import constants as const
import utils


def main():
    engine = utils.get_db_engine()
    today = utils.get_current_time()
    resp = utils.get_uri_content(uri=const.DARK_SKY_URI,
                                 content_type='json')

    for key in resp.keys():
        if isinstance(resp.get(key), dict) and 'data' in resp.get(key):
            for n, i in enumerate(resp.get(key)['data']):
                resp.get(key)['data'][n]['currentTime'] = today

    resp['currently']['lat'] = resp['latitude']
    resp['currently']['lng'] = resp['longitude']

    daily_df = pd.DataFrame(resp['daily']['data'])

    tables = ['current_weather', 'daily_weather', 'hourly_weather', 'minutely_weather']
    for table in tables:
        daily_df.to_sql(table, con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    main()
