from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/users')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form['name']
    password = generate_password_hash(request.form['password'])
    email = request.form['email']
    username = request.form['username']
    user = User(name=name, password=password, email=email, username=username)
    if user.save():
        # Flash a message
        flash("Successfully created a user", "success")
        return redirect(url_for('home'))
    else:
        #Flash a error message
        # flash("Incorrect fields. Please try again.", "danger")
        # redirect back to this page (so they can fill in form again)
        return render_template('new.html', errors=user.errors)
    

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    return render_template('edit.html', id=current_user.id, user=user)


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)

    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    
    if current_user == user:
        if name:
            user.name = name
        if email:
            user.email = email
        if username:
            user.username = username

        if user.save():
            flash("Successfully updated user information.", "success")
            return redirect(url_for('home'))
        else:
            flash("Failed to update user information.", "danger")
            return redirect(url_for('edit', id=current_user.id))
    
    if user.update(recursive=True):
        flash("", "success")
        return redirect(url_for('store_list'))
    else:
        return redirect(url_for('edit', user = user))
