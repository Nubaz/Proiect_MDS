import enum
from app import *

# Clasa rolului din baza de date
class Roles(enum.Enum):
    angajat = "angajat"
    manager = "manager"
    admin = "admin"

# Clasa utilizatorului din baza de date
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(30), nullable=False)
    prenume = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    parola = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum(Roles))

# Clasa pontajului unui angajat din baza de date
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
