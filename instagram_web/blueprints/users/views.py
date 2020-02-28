from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re
import datetime
from flask_login import current_user, login_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/create', methods=['POST'])
def create():
    em = request.form.get('email')
    us = request.form.get('username')
    pa = request.form.get('password')

    if len(pa) > 6:
        if re.search(r'[A-Z]', pa) and re.search(r'[a-z]', pa) and re.search(r'\W', pa):
            hashed_pa = generate_password_hash(pa)
            new_user = User(email=em, username=us, password=hashed_pa)

            if new_user.save():
                login_user(new_user)
                return redirect(url_for('users.index'))
            else:
                return render_template('users/new.html', errors=new_user.errors)
        else:
            return render_template('users/new.html', errors='The password requires uppercase, lowercase and at least one special character')

    else:
        return render_template('users/new.html', errors='That password is too short!')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    if 'user_id' in session:
        name = User.get(User.id == session['user_id']).username
        return render_template('users/index.html', username=name)
    else:
        return render_template('users/index.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if id == str(current_user.id):
        return render_template('users/edit.html')
    else:
        return "soz, but no access for u"


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_by_id(id)
    user.email = email
    user.username = username
    if len(password) > 0:
        if len(password) > 6:
            if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'\W', password):
                hashed_pass = generate_password_hash(password)
                user.password = hashed_pass
        else:
            return render_template('users/edit.html', errors='The password requires uppercase, lowercase and at least one special character')
    else:
        return render_template('users/edit.html', errors='That password is too short!')

    if user.save():
        flash('Updated successfully!')
        return redirect(url_for('users.edit', id=current_user.id))

    else:
        flash('failwhale')
        return render_template('users/edit.html')
