#!/bin/bash

Rscript train_model.r &&

python get_allergy_data.py &&
python get_weather_data.py &&
python get_air_data.py &&

Rscript run_model.r &&

python get_resutls_send_email.py