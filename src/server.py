from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

import os, enum

load_dotenv(find_dotenv())

app = Flask(__name__, template_folder='../templates')
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

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error_msg = ''

    if request.method == 'POST' and 'username' in request.form and 'parola' in request.form:
        username = request.form['username']
        parola = request.form['parola']

        with app.app_context():
            user = User.query.filter_by(username=username, parola=parola).all()

        if user:
            user = [u.__dict__ for u in user][0]
            session['loggedIn'] = True
            session['id'] = user['id']
            session['username'] = user['username']

            return 'Logare cu succes!'
        else:
            error_msg = 'Date de logare incorecte!'

    return render_template('login.html', error_msg=error_msg)

@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))