from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    # use User.validate_password to call the function if it's got a @classmethod. Otherwise, do newuser.validate_password to call the function

    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('users/new.html')

    newuser = User(
        username=user_name,
        email=email,
        password=hashed_password
    )

    if newuser.save():
        flash(f'Welcome {user_name}')
        return redirect(url_for('users.new'))

    else:
        flash(f'{user_name} is already taken. Pick another')
        return render_template('users/new.html', errors=newuser.errors)


# @users_blueprint.route('/<username>', methods=["GET"])
# def show(username):
#     return render_template('users/sign_in.html')

@users_blueprint.route('/signin', methods=['GET'])
def show():
    return render_template('users/sign_in.html')

# @users_blueprint.route('/', methods=["GET"])
# def index():
#     # return "USERS"
#     pass


@users_blueprint.route('/', methods=['POST'])
def signed_in(email, password):
    password_to_check = request.form['password']
    hashed_password = create.hashed_password
    result = check_password_hash(hashed_password, password_to_check)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
