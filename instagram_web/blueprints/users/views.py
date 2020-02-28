from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from models.user import User
from flask_login import current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    user = User(username=username, email=email, password=password)
    if user.save():
        flash(f"Saved user: {user.username}")
        return redirect(url_for("users.new"))
    else:
        flash(f"Some error!")
        return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    current_user.username = username
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    if not current_user.is_authenticated:
        return render_template('401.html'), 401


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/userpage.html')


@users_blueprint.route('/<id>/profile', methods=['GET'])
def profile(id):
    return render_template('users/profilepage.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(username=current_user.username)
    new_username = request.form.get("username")
    if new_username:
        user.username = new_username
    new_email = request.form.get("email")
    if new_email:
        user.email = new_email
    if user.save():
        flash("Saved!")
        return redirect(url_for("home"))
    else:
        return "error"
