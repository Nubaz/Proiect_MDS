from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import babel.dates

import os, enum

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
db = SQLAlchemy(app)


class Roles(enum.Enum):
    angajat = ("angajat",)
    manager = "manager"


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(30), nullable=False)
    prenume = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    parola = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(Roles))


class Pontaj(db.Model):
    __tablename__ = "pontaj"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ang = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    data_add = db.Column(db.DateTime, server_default="CURRENT_DATE")
    nume_pr = db.Column(db.String(50), nullable=False)
    descr_tasks = db.Column(db.Text)
    nr_ore = db.Column(db.Integer, nullable=False)
    aprobat = db.Column(db.Boolean, nullable=False, server_default="false")

    def __repr__(self):
        return str(self.id) + " " + str(self.id_ang) + " " + str(self.data_add) + " " + str(self.nume_pr) + " " + str(self.descr_tasks)


user = {}
pontaje = {}


def getPontaje():
    global pontaje

    with app.app_context():
        if session["rol"] == "angajat":
            pontaje = Pontaj.query.filter_by(id_ang=session["id"]).all()
        else:
            pontaje = Pontaj.query.all()

        if pontaje:
            for p in pontaje:
                p = p.__dict__
                p.pop("_sa_instance_state")


@app.template_filter("formatdate")
def format_datetime(value):
    return babel.dates.format_datetime(value, "EEEE, d MMM y, H:mm:s", locale="ro")


@app.route("/", methods=["GET", "POST"])
def dashboard():
    global user, pontaje

    if (request.method == "POST" and "nume-proiect" in request.form and "descriere-tasks" in request.form and "nr-ore" in request.form):
        pontaj = Pontaj(
            id_ang=session["id"],
            nume_pr=request.form["nume-proiect"],
            descr_tasks=request.form["descriere-tasks"],
            nr_ore=request.form["nr-ore"],
        )
        db.session.add(pontaj)
        db.session.commit()

        getPontaje()

    if (request.method == "POST" and "id-p-sters" in request.form):
        pontaj = Pontaj.query.filter_by(id=request.form["id-p-sters"]).one()

        db.session.delete(pontaj)
        db.session.commit()

        getPontaje()

    if (request.method == "POST" and "nume-proiect-mod" in request.form):
        pontaj = Pontaj.query.filter_by(id=request.form["id-p-mod"]).one()
        print(pontaj)
        pontaj.nume_pr = request.form["nume-proiect-mod"]
        pontaj.descr_tasks = request.form["descriere-tasks-mod"]
        pontaj.nr_ore = request.form["nr-ore-mod"]
        pontaj.data_add = datetime.today()

        print(pontaj)
        db.session.commit()

        getPontaje()

    if "loggedIn" in session:
        if session["rol"] == "angajat":
            return render_template("angajat.html", user=user, pontaje=pontaje)
        else:
            return render_template("manager.html", user=user, pontaje=pontaje)

    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    error_msg = ""

    if user:
        return redirect(url_for("dashboard"))

    if (request.method == "POST" and "username" in request.form and "parola" in request.form):
        username = request.form["username"]
        parola = request.form["parola"]

        with app.app_context():
            user = User.query.filter_by(username=username, parola=parola).all()

        if user:
            user = [u.__dict__ for u in user][0]
            session["loggedIn"] = True
            session["id"] = user["id"]
            session["username"] = user["username"]
            session["rol"] = user["rol"].value[0]

            getPontaje()

            if session["rol"] == "angajat":
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            error_msg = "Date de logare incorecte!"

    return render_template("login.html", error_msg=error_msg)


@app.route("/logout")
def logout():
    global user

    session.pop("loggedIn", None)
    session.pop("id", None)
    session.pop("username", None)
    user = {}

    return redirect(url_for("login"))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
