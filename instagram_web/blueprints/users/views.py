from flask import Flask, Blueprint, render_template, request, flash, url_for, redirect
from models.user import User

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
