from flask import Flask, redirect, url_for, flash, g
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
from app import app

# config
from app.config import Config

app.register_blueprint(views_blueprints)

login_manager = LoginManager(app)
login_manager.init_app(app)

@app.before_request
def inject_globals():
    with app.app_context():
        g.VERSION = Config.VERSION
        g.FLAG = Config.FLAG
    return None

@login_manager.user_loader
# @app.before_request
def load_user(user_id):
    return User.query.get(user_id)

api = Api(app)
api.add_resource(Prediction, '/api/1.0/prediction/')
api.add_resource(Admin, '/api/1.0/user/')

if __name__ == '__main__':
    app.run(debug=True)
