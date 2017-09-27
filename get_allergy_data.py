# get_allergy_data.py

import pandas as pd

import constants as const
import utils


# get forecast
# url = "https://www.pollen.com/api/forecast/extended/pollen/37076"
# get 30 day history
# url = 'https://www.pollen.com/api/forecast/historic/pollen/37076/30'

engine = utils.get_db_engine()
today = utils.get_current_time()
resp = utils.get_uri_content(uri=const.POLLEN_URI,
                             headers=const.POLLEN_HEADERS,
                             content_type='json')

allergens = resp['Location']['periods']

for n, row in enumerate(allergens):
    allergens[n]['Triggers'] = ', '.join([i['Name'] for i in allergens[n]['Triggers']])
    allergens[n]['dateof'] = today

allergens_df = pd.DataFrame(allergens)

allergens_df.to_sql('allergens', con=engine, if_exists='append', index=False)
