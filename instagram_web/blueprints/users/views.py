import os
from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash
from models.user import User
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('users/new.html')
    newuser = User(username=username, email=email, password=hashed_password)

    if newuser.save():
        flash("New user successfully registered!")
        return redirect(url_for('users.new'))

    else:
        flash("User registration unsuccessful")
        return render_template('users/new.html', errors=newuser.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
