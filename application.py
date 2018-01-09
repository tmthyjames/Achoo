from flask import Flask, redirect, url_for, flash, g, config, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from flask import request

# views
from app.views.views import main as views_blueprints

# forms
from app.forms.forms import LoginForm

# api
from app.api.api import Prediction, Admin

# models
from app.models.models import User

# app
from app import application

# config
from app.config import Config

application.register_blueprint(views_blueprints)

login_manager = LoginManager(application)
login_manager.init_app(application)


@application.before_request
def inject_globals():
    with application.app_context():
        session['VERSION'] = Config.VERSION
        session['MSG'] = Config.MSG
    return None

@login_manager.user_loader
# @application.before_request
def load_user(user_id):
    return User.query.get(user_id)

api = Api(application)
api.add_resource(Prediction, '/api/1.0/prediction/')
api.add_resource(Admin, '/api/1.0/user/')

if __name__ == '__main__':
    application.run()
