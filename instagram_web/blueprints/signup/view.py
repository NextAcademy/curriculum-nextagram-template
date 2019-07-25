from app import app
from flask import render_template, request, url_for,redirect, flash
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User

signup_blueprint = Blueprint('signup',
                            __name__,
                            template_folder='templates/signup')

@signup_blueprint.route("/", methods=["GET"])
def signup():
    return render_template("signup.html")


@signup_blueprint.route("/", methods=["POST", "GET"])
def create_signup():
    username = request.form.get('username') 
    password=request.form.get('password') 
    email=request.form.get('email')
    hashed_password = generate_password_hash(password)

    name = User(
        username = username,
        email = email,
        password = hashed_password
    )
    
    if name.save():
        flash(f'Welcome {username}')
        # session["user_id"] = user.id

    # hashed_password = generate_password_hash(request.form.get('password'))
    # name = User(username=request.form.get('username'), password=request.form.get(
    #     'password'), email=request.form.get('email'))

    name.save()
    # return redirect(url_for('home'))
    return render_template("home.html")
    # return f'signin'

  