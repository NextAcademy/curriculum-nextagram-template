from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    new_pw_hashed = generate_password_hash(request.form.get('new_password'))
    u = User(username=request.form.get('new_username'),
            first_name=request.form.get('new_firstname'),
            last_name=request.form.get('new_lastname'),
            email=request.form.get('new_email'),
            password=new_pw_hashed)

    if u.save():
        flash("New user created.")
        return redirect(url_for('users.new'))
    else:
        flash("Failed to create new user. Try again?")
        return render_template('users/new.html', errors=u.errors)


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
