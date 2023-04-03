from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

import os, enum

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
db = SQLAlchemy(app)

class Roles(enum.Enum):
    angajat = 'angajat',
    manager = 'manager'

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(30), nullable=False)
    prenume = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    parola = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(Roles))

    def __repr__(self):
        return f"<User id={self.id} nume={self.nume} prenume={self.prenume} username={self.username} email={self.email} parola={self.parola} rol={self.rol}>"

with app.app_context():
    print(User.query.all())


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)