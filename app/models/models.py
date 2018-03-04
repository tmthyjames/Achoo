from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import application

db = SQLAlchemy(application)
bcrypt = Bcrypt(application)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    inhaler = db.Column(db.Integer)
    meds = db.Column(db.Integer)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Treatment(UserMixin, db.Model):
    __tablename__ = 'treatment'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Float)
    lat = db.Column(db.Float)
    treatment = db.Column(db.String(100), nullable=False)
    accuracy = db.Column(db.Integer)
    zipcode = db.Column(db.String(10))

