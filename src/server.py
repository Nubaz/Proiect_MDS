from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from passlib.hash import sha256_crypt
from azure.communication.email import EmailClient

from dbModels import *
from app import *

import babel.dates
import os

def send_approval_email(angajat_email, angajat_nume):
    connection_string = ""
    try:
        client = EmailClient.from_connection_string(connection_string)
        message = {
            "content": {
                "subject": "Pontaj acceptat",
                "plainText": "Managerul a aprobat un pontaj de-al dumneavoastră.",
                "html": "<html><h1>Managerul a aprobat un pontaj de-al dumneavoastră.</h1></html>"
            },
            "recipients": {
                "to": [
                    {
                        "address": angajat_email,
                        "displayName": angajat_nume
                    }
                ]
            },
            "senderAddress": "DoNotReply@570d83fc-9db4-41d3-b929-21d2b589c84c.azurecomm.net"
        }
        response = client.begin_send(message)
        print(response)
    except Exception:
        print("Something went wrong with the email service")

user = {}
pontaje = {}

# Functie de preluare a pontajelor
# pe baza rolului utilizatorului
def getPontaje():
    global pontaje

    with app.app_context():
        if session["rol"] == "angajat":
            pontaje = Pontaj.query.filter_by(id_ang=session["id"]).all()
        else:
            pontaje = db.session.query(User, Pontaj).join(Pontaj).filter(User.id == Pontaj.id_ang).all()
            return 
           
        if pontaje:
            for p in pontaje:
                p = p.__dict__
                p.pop("_sa_instance_state")

# Functie de formatare a datei calendaristice
@app.template_filter("formatdate")
def format_datetime(value):
    return babel.dates.format_datetime(value, "EEEE, d MMM y, H:mm:s", locale="ro")

# Ruta principala
@app.route("/", methods=["GET", "POST"])
def dashboard():
    global user, pontaje

    # Operatia de aprobare a unui pontaj din BD
    if request.method == "POST" and "pontaj-id" in request.form:
        pontaj_id = request.form["pontaj-id"]
        pontaj = Pontaj.query.filter_by(id=pontaj_id).first()

        if pontaj:
            pontaj.aprobat = True
            db.session.commit()

            angajat = User.query.get(pontaj.id_ang)
            angajat_email = angajat.email
            angajat_nume = angajat.nume + angajat.prenume
            
            send_approval_email(angajat_email, angajat_nume)

            getPontaje()

    # Operatia de ADAUGARE a unui pontaj in BD
    if request.method == "POST" and "nume-proiect" in request.form and "descriere-tasks" in request.form and "nr-ore" in request.form:
        pontaj = Pontaj(
            id_ang=session["id"],
            nume_pr=request.form["nume-proiect"],
            descr_tasks=request.form["descriere-tasks"],
            nr_ore=request.form["nr-ore"],
        )
        db.session.add(pontaj)
        db.session.commit()

        getPontaje()

    # Operatia de STERGERE a unui pontaj din BD
    if request.method == "POST" and "id-p-sters" in request.form:
        pontaj = Pontaj.query.filter_by(id=request.form["id-p-sters"]).one()

        db.session.delete(pontaj)
        db.session.commit()

        getPontaje()

    # Operatia de MODIFICARE a unui pontaj din BD
    if request.method == "POST" and "nume-proiect-mod" in request.form:
        pontaj = Pontaj.query.filter_by(id=request.form["id-p-mod"]).one()
        pontaj.nume_pr = request.form["nume-proiect-mod"]
        pontaj.descr_tasks = request.form["descriere-tasks-mod"]
        pontaj.nr_ore = request.form["nr-ore-mod"]
        pontaj.data_add = datetime.today()

        db.session.commit()

        getPontaje()

    # Operatia de ADAUGARE a unui utilizator in BD
    if request.method == "POST" and "u-nume" in request.form:
        user = User(
            nume = request.form["u-nume"],
            prenume = request.form["u-prenume"],
            username = request.form["u-username"],
            email = request.form["u-email"],
            parola = sha256_crypt.hash(secret=request.form["u-parola"], salt=os.getenv("SALT")),
            rol = Roles[request.form["u-rol"][0].lower() + request.form["u-rol"][1:]],   
        )

        db.session.add(user)
        db.session.commit()

        users = db.session.query(User).all()

    # Operatia de STERGERE a utilizatorilor
    if request.method == "POST" and "u-to-delete" in request.form:
        deleted = request.form.getlist('u-to-delete')

        for toDelete in deleted:
            user = User.query.filter_by(username=toDelete).one()
            db.session.delete(user)
            db.session.commit()

        users = db.session.query(User).all()

    with app.app_context():
        users = db.session.query(User).all()
        roluri = [rol.value[0].upper()+rol.value[1:] for rol in Roles]

    # Afisarea dashboard-ului in functie de
    # tipul utilizatorului
    if "loggedIn" in session:
        if session["rol"] == "angajat":
            return render_template("angajat.html", user=user, pontaje=pontaje)
        if session["rol"] == "manager":
            return render_template("manager.html", user=user, pontaje=pontaje)
        if session["rol"] == "admin":
            return render_template("admin.html", user=user, users=users, roluri=roluri)

    # Redirectarea la pagina de logare
    # in caz ca nu exista niciun utilizator logat
    else:
        return redirect(url_for("login"))

# Ruta pentru pagina de logare
@app.route("/login", methods=["GET", "POST"])
def login():
    global user
    error_msg = ""

    if user:
        return redirect(url_for("dashboard"))

    if request.method == "POST" and "username" in request.form and "parola" in request.form:
        username = request.form["username"]
        parola = sha256_crypt.hash(secret=request.form["parola"], salt=os.getenv("SALT"))

        with app.app_context():
            user = User.query.filter_by(username=username, parola=parola).all()
            if len(user):
                user = user[0]

        if user:
            session["loggedIn"] = True
            session["id"] = user.id
            session["username"] = user.username
            session["rol"] = user.rol.name

            getPontaje()

            return redirect(url_for("dashboard"))
        else:
            error_msg = "Date de logare incorecte!"

    return render_template("login.html", error_msg=error_msg)

# Ruta pentru delogare
@app.route("/logout")
def logout():
    global user

    session.pop("loggedIn", None)
    session.pop("id", None)
    session.pop("username", None)
    user = {}

    return redirect(url_for("login"))

# Ruta pentru eroarea HTTP 404
@app.errorhandler(404)
def not_found(e):
    if "logged_in" in session:
        return render_template("404.html")
    else:
        return redirect(url_for("login"))