# treatments.py

import RPi.GPIO as GPIO
import time
import datetime
import os
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://'+os.environ['USERNAME']+':'+os.environ['PASSWORD']+'@'+os.environ['HOSTNAME']+':5432/allergyalert')

inhaler_btn = 18
breathing_treatment_btn = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(inhaler_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(breathing_treatment_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

treatment = 0
today = time.mktime(datetime.datetime.now().timetuple())
while True:
    timeof=datetime.datetime.now().timetuple()
    if(GPIO.input(inhaler_btn) == GPIO.LOW):
        print ("Inhaler was used...")
        today = time.mktime(datetime.datetime.now().timetuple())
        treatment = 1
    elif(GPIO.input(breathing_treatment_btn) == GPIO.LOW):
        print ("Breathing treament was administered...")
        today = time.mktime(datetime.datetime.now().timetuple())
        treatment = 2
    if treatment:
        treatment_df = pd.DataFrame([{'treatment': treatment, 'dateof': today}])
        treatment_df.to_sql('treatments', con=engine, if_exists='append', index=False)
    if not treatment and timeof.tm_hour == 22 and timeof.tm_min == 30:
        treatment_df = pd.DataFrame([{'treatment': treatment, 'dateof': today}])
        treatment_df.to_sql('treatments', con=engine, if_exists='append', index=False)
    treatment = 0
    time.sleep(0.1)
