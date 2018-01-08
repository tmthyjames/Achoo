from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['ACHOO_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['ACHOO_PG_CONN_STR']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
