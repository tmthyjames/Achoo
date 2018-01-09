# treatment_tracker.py

import time

import pandas as pd
import RPi.GPIO as GPIO

import munging.utils as utils


def main():
    engine = utils.get_db_engine()

    inhaler_btn = 18
    breathing_treatment_btn = 23

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(inhaler_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(breathing_treatment_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    treatment = 0
    today = utils.get_current_time()
    while True:
        timeof = utils.get_current_time(no_wrap=True)
        if GPIO.input(inhaler_btn) == GPIO.LOW:
            print("Inhaler was used...")
            today = utils.get_current_time()
            treatment = 1
        elif GPIO.input(breathing_treatment_btn) == GPIO.LOW:
            print("Breathing treament was administered...")
            today = utils.get_current_time()
            treatment = 2
        if treatment:
            treatment_df = pd.DataFrame([{'treatment': treatment, 'dateof': today}])
            treatment_df.to_sql('treatments', con=engine, if_exists='append', index=False)
        if not treatment and timeof.tm_hour == 22 and timeof.tm_min == 30:
            treatment_df = pd.DataFrame([{'treatment': treatment, 'dateof': today}])
            treatment_df.to_sql('treatments', con=engine, if_exists='append', index=False)
        treatment = 0
        time.sleep(0.1)


if __name__ == '__main__':
    main()
