from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User
from flask_login import login_required


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User(
        full_name=full_name,
        email=email,
        username=username,
        password=password
    )

    if user.save():
        flash('Successfully created new account', 'success')
        return redirect(url_for('home'))

    if user.errors:
        for error in user.errors:
            flash(f'{error}', 'warning')
        return redirect(url_for('home'))
    else:
        flash('Oops something went wrong!', 'warning')
        return redirect(url_for('home'))


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('users/index.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
