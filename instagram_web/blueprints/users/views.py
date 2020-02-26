from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash
import re


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    em = request.form.get('email')
    us = request.form.get('username')
    pa = request.form.get('password')

    if len(pa) > 6:
        if re.search(r'[A-Z]', pa) and re.search(r'[a-z]', pa) and re.search(r'\W', pa):
            hashed_pa = generate_password_hash(pa)

            new_user = User(email=em, username=us, password=hashed_pa)

            if new_user.save():
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
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
