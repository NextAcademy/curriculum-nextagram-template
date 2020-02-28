
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


# GET IT TO SHOW new.html


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    new_name = request.form.get("new_name")
    new_email = request.form.get("new_email")
    new_password = request.form.get("new_password")
    # hashed_password = generate_password_hash(new_password)

    new_user = User(name=new_name, email=new_email,
                    password=new_password)  # hashes password

    if new_user.save():
        flash(f"Saved new User: {new_name}")
        return redirect(url_for("users.new"))
    else:
        flash("Error during signup, please refer to error message")
        return render_template("users/new.html", errors=new_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.name == username)

    if current_user:
        if not user:
            flash(f"You're in the wrong neighborhood boy")
            return redirect(url_for("home"))
        else:
            return render_template("users/show.html", user=user)
    else:
        return abort(401)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)

    if current_user:
        if not user:
            flash(f"You're in the wrong neighborhood boy")
            return redirect(url_for("home"))
        else:
            return render_template("users/edit.html", user=user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    if not str(current_user.id) == id:
        flash(f"You are not authorized to update this page")
        return redirect(url_for('users.edit', id=id))

    user = User.get_or_none(User.id == id)

    if current_user:
        if not user:
            flash(f"You're in the wrong neighborhood boy")
            return redirect(url_for("users.edit"))
        else:
            new_name = request.form.get("new_name")
            new_email = request.form.get("new_email")

            user.name = new_name
            user.email = new_email

            if user.save():
                flash(f"User edits successfully made")
                return redirect(url_for("users.edit", id=user.id))
            else:
                return render_template('users/edit.html', errors=user.errors)
            # pass handles the logic?? validation for both edit and update?
    # else:
    #     return abort(401)
