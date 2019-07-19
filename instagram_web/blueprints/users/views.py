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
    user = User.get_or_none(User.username == username)

    if not user:
        flash('No such user found', 'warning')
        return redirect(url_for('users.index'))

    return render_template('users/show.html', user=user)


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('users/index.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    if not user:
        flash('No such user exists!', 'warning')
        return redirect(url_for('users.index'))
    return render_template('users/edit.html', user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
