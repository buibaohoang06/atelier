from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import app

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    hashed_password = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    caption = db.Column(db.String(), unique=True, nullable=False, default="This is my introduction.")
    realname = db.Column(db.String(), unique=False, nullable=False)

class Images(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    image_id = db.Column(db.String(), nullable=False, unique=True)
    image_address = db.Column(db.String(), nullable=False, unique=True)
    image_owner = db.Column(db.String(), nullable=False, unique=False)
    creation_date = db.Column(db.String(), nullable=False, unique=False)
    description = db.Column(db.String(), nullable=False, unique=True)

class Wallet(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    owner = db.Column(db.String(), unique=True, nullable=False)
    wallet_id = db.Column(db.String(), unique=True, nullable=False)
    balance = db.Column(db.Integer(), unique=True, nullable=False, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    sender = db.Column(db.String(), unique=False, nullable=False)
    recipient = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer(), unique=False, nullable=False, default=0)
