from flask import Blueprint, render_template, redirect, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired
from hashlib import md5
import uuid
from sqlite3 import IntegrityError
from models import db, User
from app import app

#Initialize Blueprint
authbp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates", static_folder="static")

#Hashing functionalities
def hashing(data):
    return md5(data.encode('utf-8')).hexdigest()

def checkhash(data: str, compare: str):
    return hashing(data=data) == compare

#Forms
class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField()

class RegisterForm(FlaskForm):
    uusername = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    email = EmailField(validators=[InputRequired()], render_kw={"placeholder": "E-mail"})
    realname = StringField(validators=[InputRequired()], render_kw={"placeholder": "Full Name"})
    submit = SubmitField()

#Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

#Routes
@authbp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/marketplace')
    form = LoginForm()
    if form.validate_on_submit():
        try:
            check_user = User.query.filter_by(email=form.email.data).first()
            if checkhash(data=form.password.data, compare=check_user.hashed_password):
                login_user(check_user)
                flash("Logged in!", 'success')
                return redirect('/marketplace')
            else:
                flash("Wrong password!", 'danger')
                return redirect('/auth/login')
        except AttributeError:
            db.session.rollback()
            flash("Unable to find user with that username", 'danger')
            return redirect('/auth/login')
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong!", 'danger')
            print(str(e))
            return redirect('/auth/login')
    return render_template('login.html', form=form)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/marketplace')
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = User(user_id=str(uuid.uuid1()), username=form.username.data, hashed_password=hashing(data=form.password.data), email=form.email.data, realname=form.realname.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered! Please login to continue!", 'success')
            return redirect('/auth/login')
        except IntegrityError:
            db.session.rollback()
            flash("An user has already registered with that information!", 'danger')
            return redirect('/auth/register')
        except Exception as e:
            db.session.rollback()
            print(str(e))
            flash("Something went wrong!", 'danger')
            return redirect('/auth/register')
    return render_template('register.html', form=form)

@authbp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/auth/login')
