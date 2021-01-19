from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import login_required, login_user, current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    params = request.form

    new_user = User(username=params.get("username"), email=params.get("email"), password=params.get("password"))

    if new_user.save():
        flash("Successfully signed up")
        return redirect(url_for("home"))
    else:
        flash(new_user.errors)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    if user:  
        return render_template("users/show.html", user=user)
    else:
        flash("No user found")
        return redirect(url_for("home")) 


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user=user)
        else:
            flash("Cannot edit someone else's profile")
            return redirect(url_for('users.show', username=username))
    else:
        flash("No user found")
        return redirect(url_for("home"))


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == id)
    if user: 
        if current_user.id == int(id):
            params = request.form

            user.username = params.get("username")
            user.email = params.get("email") 
            print("user.email")
            password = params.get("password")

            if len(password) > 0:
                user.password = password
                
            if user.save():
                flash("Successfully updated details")
                return redirect(url_for("users.show", username=user.username))
            else: 
                flash("Failed to edit the details. Try again.")
                return redirect(url_for("users.edit", id=user.id))
        
        else:
            flash("You cannot edit details of another user")
            return redirect(url_for("home"))
    else:
        flash("No such user found")
        return redirect(url_for("home"))