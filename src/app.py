from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
db = SQLAlchemy(app)