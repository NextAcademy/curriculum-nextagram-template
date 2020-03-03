from flask import Flask, Blueprint, session, render_template, request, flash, url_for, redirect
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/login', methods=['GET', 'POST'])
def create():
    username = request.form.get("username")
    password = request.form.get("password")
    user_exist = User.get_or_none(User.username == username)

    if not user_exist:
        flash("That user does not exist. Please check your details")
        return redirect(url_for('home'))

    password_to_check = user_exist.password

    if not check_password_hash(password_to_check, password):
        flash("Something wrong with your password. Please double check again.")
        return redirect(url_for("home"))

    login_user(user_exist)
    flash(f"You are now logged in! Hi {username}!")
    return redirect(url_for("home"))


@sessions_blueprint.route("/logout", methods=['GET'])
def logout():
    logout_user()
    flash("You are now logged out!")
    return redirect(url_for('main'))

    # if user_exist:
    #     login_user = User.get(User.username == username)
    #     hashed_password = login_user.password
    #     # Check password whether correct
    #     result = check_password_hash(hashed_password, password)
    #     if result:
    #         session['username'] = login_user.email
    #         return redirect(url_for('sessions.new'))
    #     else:
    #         flash("Incorrect Email or Password")
    #         return redirect(url_for("sessions.new"))
    # else:
    #     flash("Email Does Not Exist")
    #     return redirect(url_for('sessions.new'))


# @users_blueprint.route('/<username>', methods=["GET"])
# def show(username):
#     pass


# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"


# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass


# @users_blueprint.route('/<id>', methods=['POST'])
# def update(id):
#     pass
