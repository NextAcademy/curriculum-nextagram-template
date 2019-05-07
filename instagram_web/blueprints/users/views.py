from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)

    # use User.validate_password to call the function if it's got a @classmethod. Otherwise, do newuser.validate_password to call the function

    if not User.validate_password(password):
        flash(f'Password invalid')
        return render_template('new.html')

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
        return render_template('new.html', errors=newuser.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show():
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    # return "USERS"
    pass


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('edit_user.html')
    else:
        flash('You are not authorized to do this!')
        return redirect(url_for('home'))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    if not current_user == user:
        flash('You are not authorized to do this!')
        return render_template('edit_user.html', user=user)

    else:
        new_user_name = request.form.get('new_user_name')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')

    # use update because using save will execute the validation in users.py
        update_user = User.update(
            username=new_user_name,
            email=new_email,
            password=new_password
        ).where(User.id == id)

        if not update_user.execute():
            flash(
                f'Unable to update, please try again')
            return render_template('edit_user.html', user=user)

        flash('Successfully updated')
        return redirect(url_for('home'))
