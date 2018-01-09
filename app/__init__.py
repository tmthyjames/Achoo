from flask import Flask
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['ACHOO_SECRET_KEY']
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['ACHOO_PG_CONN_STR']
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
