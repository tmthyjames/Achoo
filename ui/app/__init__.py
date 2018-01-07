from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tdobbins:1q2w3e4r5t6y@localhost:5432/achoo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
