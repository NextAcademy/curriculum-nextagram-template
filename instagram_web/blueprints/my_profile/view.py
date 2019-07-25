from app import app
from flask import render_template, request, url_for,redirect, flash
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import current_user

myprofile_blueprint = Blueprint('my_profile',
                            __name__,
                            template_folder='templates')

@myprofile_blueprint.route("/", methods=["GET"])
def index():
  
    if(current_user.is_authenticated):
        return render_template("my_profile.html")
    else:
        return render_template("signin.html")