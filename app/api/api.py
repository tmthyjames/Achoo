import os
from flask_restful import Resource
from flask import request, url_for
from flask_login import current_user, login_user

import requests
import json

# models
from app.models.models import User, db, bcrypt, Treatment

class Prediction(Resource):

    def get(self):
        return {'hello': 'world'}

    def post(self):
        capture_data = request.get_json()
        latitude = capture_data.get('coords').get('latitude')
        longitude = capture_data.get('coords').get('longitude')
        timestamp = capture_data.get('timestamp')
        treatment = capture_data.get('treatment')
        accuracy = capture_data.get('accuracy')

        treatment = Treatment(
            userid=current_user.id,
            timestamp=timestamp,
            lat=latitude,
            lng=longitude,
            treatment=treatment,
            accuracy=accuracy
        )
        db.session.add(treatment)
        db.session.commit()

        return {'status': 200}

class Admin(Resource):

    def post(self):
        signup_data = request.get_json()
        zipcode = signup_data.get('zipcode')
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+str(zipcode)+'&key=' + os.environ['ACHOO_GOOGLE_MAPS_API_KEY'])

        location = json.loads(r.content)['results'][0]['geometry']['location']
        lat = location.get('lat')
        lng = location.get('lng')

        user = User(
            username=signup_data.get('username'),
            email=signup_data.get('email'),
            inhaler=signup_data.get('inhaler') or 0,
            zipcode=zipcode,
            meds=signup_data.get('meds') or 0,
            lat=lat,
            lng=lng
        )
        user.set_password(signup_data.get('password'))
        db.session.add(user)
        db.session.commit()
        login_user(user)

        return {'status': 200, 'location': url_for('main.capture')}
