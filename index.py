from flask import Blueprint, render_template, redirect, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired

#Initialize Blueprint
indexbp = Blueprint("index", __name__, static_folder="static", template_folder="templates", url_prefix="/")

#Routes
@indexbp.route('/', methods=['GET'])
def indexpage():
    return render_template('index.html')